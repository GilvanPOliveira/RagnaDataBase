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