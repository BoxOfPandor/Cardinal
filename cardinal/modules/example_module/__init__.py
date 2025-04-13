"""
Example module for Cardinal.
"""

from .routes import router

# This is important for auto-discovery
__all__ = ["router"]