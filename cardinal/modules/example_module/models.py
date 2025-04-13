"""
Data models for the example module.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    """Base class for Item models."""
    name: str = Field(..., description="Name of the item", example="Example Item")
    description: Optional[str] = Field(None, description="Description of the item", example="This is an example item")
    price: float = Field(..., description="Price of the item", example=19.99, ge=0)
    is_active: bool = Field(True, description="Whether the item is active")

class ItemCreate(ItemBase):
    """Model for creating a new item."""
    pass

class ItemUpdate(BaseModel):
    """Model for updating an existing item."""
    name: Optional[str] = Field(None, description="Name of the item")
    description: Optional[str] = Field(None, description="Description of the item")
    price: Optional[float] = Field(None, description="Price of the item", ge=0)
    is_active: Optional[bool] = Field(None, description="Whether the item is active")

class Item(ItemBase):
    """Model for an item."""
    id: int = Field(..., description="Unique identifier for the item")
    created_at: datetime = Field(..., description="When the item was created")
    updated_at: Optional[datetime] = Field(None, description="When the item was last updated")
    
    class Config:
        """Configuration for the model."""
        orm_mode = True