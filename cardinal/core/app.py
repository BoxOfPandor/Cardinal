"""
Main FastAPI application factory for Cardinal.
"""

import logging
from fastapi import FastAPI, APIRouter
from .module_loader import ModuleLoader
from .config import CoreConfig

logger = logging.getLogger(__name__)

def create_app(config: CoreConfig = None) -> FastAPI:
    """
    Create and configure a FastAPI application instance.

    Args:
        config: Configuration for the application. If None, default config is used.

    Returns:
        A configured FastAPI application instance.
    """
    if config is None:
        config = CoreConfig()

    # Create FastAPI app with metadata
    app = FastAPI(
        title=config.app_name,
        description=config.description,
        version=config.version,
        docs_url=config.docs_url,
        redoc_url=config.redoc_url,
        openapi_url=config.openapi_url,
    )

    # Create main router
    main_router = APIRouter()

    # Add health check endpoint
    @main_router.get("/health", tags=["System"])
    async def health_check():
        return {"status": "healthy", "version": config.version}
    
    # Create and setup module loader
    module_loader = ModuleLoader(app, config.modules_path)

    # Add modules info endpoint
    @main_router.get("/modules", tags=["System"])
    async def modules_info():
        """Return information about all loaded modules."""
        modules_data = []
        
        for module_name, module in module_loader.loaded_modules.items():
            router = module_loader._get_module_router(module)
            routes_count = 0
            prefix = ""
            
            if router:
                prefix = getattr(router, "prefix", "")
                # Count routes associated with this router
                for route in app.routes:
                    if hasattr(route, "path") and route.path.startswith(prefix or "/"):
                        if not prefix or (
                            # Ensure we only count routes that belong to this router
                            # and not routes that just happen to start with the same prefix
                            prefix == "/" or 
                            route.path == prefix or 
                            route.path.startswith(f"{prefix}/")
                        ):
                            routes_count += 1
            
            # Get module description if available
            description = getattr(module, "__doc__", "").strip() or "No description available"
            
            modules_data.append({
                "name": module_name,
                "route_prefix": prefix,
                "routes_count": routes_count,
                "description": description,
                "is_active": True  # All loaded modules are active
            })
        
        return {"modules": modules_data}

    # Include the main router
    app.include_router(main_router)

    # Load initial modules
    module_loader.load_all_modules()

    # Store module_loader in app state for access from other parts
    app.state.module_loader = module_loader

    # Add event handlers
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting Cardinal {config.version}")
        if config.auto_reload:
            await module_loader.start_watcher()

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down Cardinal")
        if config.auto_reload:
            await module_loader.stop_watcher()

    return app