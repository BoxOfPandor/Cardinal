"""
Logging configuration for Cardinal.
"""

import logging
import sys
import os
from typing import Optional
from fastapi import FastAPI
from pathlib import Path

def setup_logging(app: Optional[FastAPI] = None, log_level: str = "INFO",
                  log_format: str = None, log_file: str = None) -> logging.Logger:
    """
    Configure logging for Cardinal.

    Args:
        app: FastAPI application instance
        log_level: Logging level to use
        log_format: Format string for log messages
        log_file: Path to log file

    Returns:
        Configured logger instance
    """
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Use default format if none provided
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Create logger for Cardinal
    logger = logging.getLogger("cardinal")
    logger.setLevel(numeric_level)
    logger.handlers = []  # Clear existing handlers

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler if log_file is specified
    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Configure basic logging
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # If app is provided, add logging middleware
    if app:
        @app.middleware("http")
        async def log_requests(request, call_next):
            logger.debug(f"Request: {request.method} {request.url.path}")
            response = await call_next(request)
            logger.debug(f"Response: {response.status_code}")
            return response

    return logger