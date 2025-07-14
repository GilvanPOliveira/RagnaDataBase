from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime

class ListCreate(BaseModel):
    name: str

class ListItemCreate(BaseModel):
    item_id: int
    quantity: int

class BulkListItemCreate(BaseModel):
    items: List[ListItemCreate]

class UpdateListItem(BaseModel):
    quantity: int

class SoldBy(BaseModel):
    npc_name: str
    map: str
    coordinates: str
    price: int

class LowestUserOffer(BaseModel):
    price: int
    user_name: str
    user_email: EmailStr

class DropMonster(BaseModel):
    monster_name: str
    map: str
    drop_rate: str
    qtd_mob: int

class ListItemResponse(BaseModel):
    item_id: int
    name: str
    image_collection: Optional[str]
    qtd_item: int
    sold_by: List[SoldBy]
    lowest_user_offer: Optional[LowestUserOffer]
    drop_monsters: List[DropMonster]

    # Pydantic v2: Configuração de atributos diretamente na classe
    model_config = ConfigDict(from_attributes=True)

class ListRead(BaseModel):
    id: int
    local_id: int
    name: str
    created_at: datetime
    updated_at: datetime
    items: List[ListItemResponse] = []

    # Pydantic v2: Configuração de atributos diretamente na classe
    model_config = ConfigDict(from_attributes=True)
