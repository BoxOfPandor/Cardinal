"""
Module discovery and loading for Cardinal.
"""

import os
import sys
import importlib
import importlib.util
import inspect
import logging
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from fastapi import FastAPI, APIRouter

logger = logging.getLogger(__name__)

class ModuleLoader:
    """
    Handles the discovery, loading, and hot-reloading of Cardinal modules.
    """

    def __init__(self, app: FastAPI, modules_path: str):
        """
        Initialize the ModuleLoader.

        Args:
            app: The FastAPI application instance
            modules_path: Path to the directory containing modules
        """
        self.app = app
        self.modules_path = Path(modules_path)
        self.loaded_modules: Dict[str, Any] = {}
        self.watcher_task = None
        self.running = False

        # Ensure the modules directory exists
        if not self.modules_path.exists():
            logger.warning(f"Modules directory {self.modules_path} does not exist. Creating it.")
            self.modules_path.mkdir(parents=True)

    def discover_modules(self) -> List[str]:
        """
        Discover available modules in the modules directory.

        Returns:
            A list of module names.
        """
        modules = []

        # Look for directories that contain an __init__.py file
        for item in self.modules_path.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                modules.append(item.name)

        return modules

    def load_module(self, module_name: str) -> bool:
        """
        Load a specific module and register its routes.

        Args:
            module_name: Name of the module to load

        Returns:
            True if the module was loaded successfully, False otherwise.
        """
        try:
            # Full import path for the module
            full_module_path = f"{self.modules_path.name}.{module_name}"

            # Check if the module was previously loaded
            if module_name in self.loaded_modules:
                # Try to reload the module
                logger.info(f"Reloading module: {module_name}")

                # Remove existing routes if any
                if hasattr(self.loaded_modules[module_name], "router"):
                    self._unregister_module_routes(module_name)

                # Remove from sys.modules to force a fresh import
                self._cleanup_module_from_sys(full_module_path)

            # Import the module
            module = importlib.import_module(full_module_path)

            # Reload to ensure we get the latest version
            module = importlib.reload(module)

            # Store the module
            self.loaded_modules[module_name] = module

            # Look for a router attribute or instance
            router = self._get_module_router(module)

            if router:
                # Include the router in the app
                logger.info(f"Registering routes for module: {module_name}")
                self.app.include_router(router)
                return True
            else:
                logger.warning(f"No router found in module: {module_name}")
                return False

        except Exception as e:
            logger.error(f"Error loading module {module_name}: {str(e)}")
            return False

    def _get_module_router(self, module) -> Optional[APIRouter]:
        """
        Extract the router from a module.

        Args:
            module: The imported module

        Returns:
            The APIRouter if found, None otherwise.
        """
        # First check if the module has a direct router attribute
        if hasattr(module, "router"):
            return module.router

        # Then check if the router is in routes.py
        if hasattr(module, "routes") and hasattr(module.routes, "router"):
            return module.routes.router

        # Look for APIRouter instances in the module's attributes
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, APIRouter):
                return attr

        return None

    def _unregister_module_routes(self, module_name: str) -> None:
        """
        Unregister routes for a module.

        Args:
            module_name: Name of the module
        """
        module = self.loaded_modules.get(module_name)
        if not module:
            return

        router = self._get_module_router(module)
        if not router:
            return

        # Find and remove routes from the app
        routes_to_remove = []
        prefix = getattr(router, "prefix", "")

        for route in self.app.routes:
            # Check if this route belongs to the module
            if hasattr(route, "path") and route.path.startswith(prefix):
                routes_to_remove.append(route)

        # Remove the routes
        for route in routes_to_remove:
            self.app.routes.remove(route)

        logger.info(f"Unregistered {len(routes_to_remove)} routes for module: {module_name}")

    def _cleanup_module_from_sys(self, module_path: str) -> None:
        """
        Remove a module and its submodules from sys.modules to force reload.

        Args:
            module_path: Full import path of the module
        """
        modules_to_remove = [
            m for m in sys.modules if m == module_path or m.startswith(f"{module_path}.")
        ]

        for m in modules_to_remove:
            if m in sys.modules:
                del sys.modules[m]

    def load_all_modules(self) -> None:
        """
        Discover and load all available modules.
        """
        modules = self.discover_modules()
        logger.info(f"Discovered modules: {modules}")

        for module_name in modules:
            success = self.load_module(module_name)
            if success:
                logger.info(f"Successfully loaded module: {module_name}")
            else:
                logger.error(f"Failed to load module: {module_name}")

    async def watch_modules(self) -> None:
        """
        Watch for changes in the modules directory and reload modules as needed.
        This is a simple polling implementation. For production, consider using a file
        system watcher library.
        """
        last_scan = {}
        self.running = True

        while self.running:
            try:
                # Check each module directory for changes
                for module_dir in self.modules_path.iterdir():
                    if not module_dir.is_dir() or not (module_dir / "__init__.py").exists():
                        continue

                    module_name = module_dir.name
                    latest_modification = 0

                    # Find the newest modification time in the module directory
                    for root, _, files in os.walk(module_dir):
                        for file in files:
                            if file.endswith('.py'):
                                file_path = os.path.join(root, file)
                                mod_time = os.path.getmtime(file_path)
                                latest_modification = max(latest_modification, mod_time)

                    # If this is a new module or has been modified, reload it
                    if module_name not in last_scan or latest_modification > last_scan[module_name]:
                        last_scan[module_name] = latest_modification
                        logger.info(f"Change detected in module: {module_name}")
                        self.load_module(module_name)

                # Check for new modules
                modules = self.discover_modules()
                new_modules = [m for m in modules if m not in self.loaded_modules]
                for module_name in new_modules:
                    logger.info(f"New module detected: {module_name}")
                    self.load_module(module_name)

                # Sleep to prevent high CPU usage
                await asyncio.sleep(2)

            except Exception as e:
                logger.error(f"Error in module watcher: {str(e)}")
                await asyncio.sleep(5)  # Sleep longer on error

    async def start_watcher(self) -> None:
        """
        Start the file watcher for hot reloading modules.
        """
        logger.info("Starting module watcher")
        self.watcher_task = asyncio.create_task(self.watch_modules())

    async def stop_watcher(self) -> None:
        """
        Stop the file watcher.
        """
        if self.running:
            logger.info("Stopping module watcher")
            self.running = False
            if self.watcher_task:
                self.watcher_task.cancel()
                try:
                    await self.watcher_task
                except asyncio.CancelledError:
                    pass