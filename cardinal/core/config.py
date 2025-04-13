"""
Configuration management for Cardinal core.
"""

import os
from pydantic import BaseSettings
from typing import Optional
from pathlib import Path

class CoreConfig(BaseSettings):
    """
    Configuration settings for Cardinal core.

    Attributes:
        app_name: Name of the application
        description: Description of the application
        version: Version of the application
        modules_path: Path to the modules directory
        auto_reload: Whether to automatically reload modules on changes
        docs_url: URL for the Swagger UI documentation
        redoc_url: URL for the ReDoc documentation
        openapi_url: URL for the OpenAPI schema
        log_level: Log level for the application
        log_format: Format string for logs
        log_file: Path to the log file
    """
    app_name: str = "Cardinal API"
    description: str = "A modular, extensible API framework"
    version: str = "0.1.0"
    modules_path: str = "modules"
    auto_reload: bool = True
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = "logs/cardinal.log"

    class Config:
        """Configuration for the settings class"""
        env_prefix = "CARDINAL_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    def dict(self, *args, **kwargs):
        """Override dict to make it safe for logging."""
        # Exclude sensitive fields from logging if needed
        result = super().dict(*args, **kwargs)
        # Example: if 'secret_key' in result:
        #     result['secret_key'] = '***'
        return result