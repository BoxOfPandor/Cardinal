"""
API routes for the example module.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List, Optional
from .models import Item, ItemCreate, ItemUpdate
from .services import ItemService

# Create router with prefix and tags
router = APIRouter(prefix="/items", tags=["Items"])

# Initialize service
item_service = ItemService()

@router.get("/", response_model=List[Item])
async def get_items(skip: int = 0, limit: int = 10):
    """
    Get a list of items with pagination.
    """
    return item_service.get_items(skip=skip, limit=limit)

@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """
    Create a new item.
    """
    return item_service.create_item(item)

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int = Path(..., description="The ID of the item to get")):
    """
    Get a specific item by ID.
    """
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_update: ItemUpdate,
    item_id: int = Path(..., description="The ID of the item to update")
):
    """
    Update an existing item.
    """
    item = item_service.update_item(item_id, item_update)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int = Path(..., description="The ID of the item to delete")):
    """
    Delete an item.
    """
    success = item_service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None