"""
Business logic for the example module.
"""

from typing import List, Optional, Dict
from datetime import datetime
from .models import Item, ItemCreate, ItemUpdate

class ItemService:
    """
    Service for managing items.
    
    In a real application, this would interact with a database.
    For simplicity, this example uses an in-memory dictionary.
    """
    
    def __init__(self):
        """Initialize the service with some example data."""
        self.items: Dict[int, Item] = {
            1: Item(
                id=1,
                name="Example Item 1",
                description="This is the first example item",
                price=19.99,
                is_active=True,
                created_at=datetime.now()
            ),
            2: Item(
                id=2,
                name="Example Item 2",
                description="This is the second example item",
                price=29.99,
                is_active=True,
                created_at=datetime.now()
            )
        }
        self.counter = 3  # Next ID to assign
    
    def get_items(self, skip: int = 0, limit: int = 10) -> List[Item]:
        """
        Get a list of items with pagination.
        
        Args:
            skip: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            A list of items
        """
        items = list(self.items.values())
        return items[skip:skip + limit]
    
    def get_item(self, item_id: int) -> Optional[Item]:
        """
        Get a specific item by ID.
        
        Args:
            item_id: ID of the item to get
            
        Returns:
            The item if found, None otherwise
        """
        return self.items.get(item_id)
    
    def create_item(self, item_create: ItemCreate) -> Item:
        """
        Create a new item.
        
        Args:
            item_create: Data for the new item
            
        Returns:
            The created item
        """
        # Create a new item with an incremented ID
        item = Item(
            id=self.counter,
            **item_create.dict(),
            created_at=datetime.now()
        )
        
        # Add it to our "database"
        self.items[self.counter] = item
        self.counter += 1
        
        return item
    
    def update_item(self, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
        """
        Update an existing item.
        
        Args:
            item_id: ID of the item to update
            item_update: New data for the item
            
        Returns:
            The updated item if found, None otherwise
        """
        # Check if the item exists
        if item_id not in self.items:
            return None
        
        # Get the existing item
        item = self.items[item_id]
        
        # Update only the fields that are provided
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        
        # Update the updated_at timestamp
        item.updated_at = datetime.now()
        
        # Store the updated item
        self.items[item_id] = item
        
        return item
    
    def delete_item(self, item_id: int) -> bool:
        """
        Delete an item.
        
        Args:
            item_id: ID of the item to delete
            
        Returns:
            True if the item was deleted, False if not found
        """
        if item_id not in self.items:
            return False
            
        del self.items[item_id]
        return True