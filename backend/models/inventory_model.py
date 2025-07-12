from pydantic import BaseModel, Field
from typing import Optional

class InventoryCreate(BaseModel):
    item_id: int
    item_name: str
    image_collection: Optional[str]
    quantity: int = Field(gt=0)
    price: int = Field(ge=0)

class InventoryPublic(BaseModel):
    item_id: int
    item_name: str
    image_collection: Optional[str]
    quantity: int
    price: int
    user: dict 

class InventoryUpdate(BaseModel):
    price: Optional[float]
    quantity: Optional[int]

class InventoryBatchUpdate(BaseModel):
    item_id: int
    quantity: Optional[int] = None
    price: Optional[int] = None