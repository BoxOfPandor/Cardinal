# main.py
"""
Main entry point for Cardinal API.
"""

import os
import logging
from core import create_app
from core.config import CoreConfig
from core.utils import setup_logging, setup_error_handlers

# Load configuration
config = CoreConfig()

# Configure logging
logger = setup_logging(
    log_level=config.log_level,
    log_format=config.log_format,
    log_file=config.log_file
)

# Create the FastAPI application
app = create_app(config)

# Setup error handlers
setup_error_handlers(app)

logger.info(f"Cardinal initialized with config: {config.dict()}")
