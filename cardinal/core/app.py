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

    # Include the main router
    app.include_router(main_router)

    # Create and setup module loader
    module_loader = ModuleLoader(app, config.modules_path)

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