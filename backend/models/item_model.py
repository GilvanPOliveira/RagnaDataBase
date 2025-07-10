from typing import List, Optional
from pydantic import BaseModel, Field

class ItemSetEntry(BaseModel):
    itemId: int
    name: str

class ItemSet(BaseModel):
    name: str
    items: List[ItemSetEntry]

class ItemSummonInfo(BaseModel):
    sourceId: int
    sourceName: str
    targetId: int
    targetName: str
    chance: Optional[float] = Field(default=None)

class SoldByEntry(BaseModel):
    npc_name: str
    map: Optional[str] = None
    x: int
    y: int
    price: int

class ContainedInEntry(BaseModel):
    source_name: str
    chance: Optional[float] = Field(default=None)

class ItemModel(BaseModel):
    # Identificadores e nomes
    id: int
    aegisName: str
    name: str
    unidName: Optional[str] = Field(default=None)
    resName: Optional[str] = Field(default=None)
    unidResName: Optional[str] = Field(default=None)

    # Descrições
    description: Optional[str] = Field(default=None)
    unidDescription: Optional[str] = Field(default=None)
    description_text: Optional[str] = Field(default=None)

    # Informações visuais
    image_icon: Optional[str] = Field(default=None)
    image_collection: Optional[str] = Field(default=None)

    # Dados básicos
    slots: Optional[int] = Field(default=None)
    setname: Optional[str] = Field(default=None)
    itemTypeId: Optional[int] = Field(default=None)
    itemSubTypeId: Optional[int] = Field(default=None)
    itemLevel: Optional[int] = Field(default=None)

    # Requisitos e atributos
    attack: Optional[int] = Field(default=None)
    matk: Optional[int] = Field(default=None)
    defense: Optional[int] = Field(default=None)
    weight: Optional[float] = Field(default=None)
    requiredLevel: Optional[int] = Field(default=None)
    limitLevel: Optional[int] = Field(default=None)
    weapon_level: Optional[int] = Field(default=None)
    property: Optional[str] = Field(default=None)
    usable_by: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    subtype: Optional[str] = Field(default=None)
    added_date: Optional[str] = Field(default=None)
    gender: Optional[int] = Field(default=None)
    range: Optional[int] = Field(default=None)
    attribute: Optional[int] = Field(default=None)

    # Composição e posição
    location: Optional[str] = Field(default=None)
    compositionPos: Optional[str] = Field(default=None)
    accessory: Optional[str] = Field(default=None)
    EQUIP: Optional[int] = Field(default=None)
    LOCA: Optional[int] = Field(default=None)

    # Status booleanos
    refinable: Optional[bool] = Field(default=None)
    indestructible: Optional[bool] = Field(default=None)
    hasScript: Optional[bool] = Field(default=None)

    # Preço e comércio
    price: Optional[int] = Field(default=None)
    drop: Optional[bool] = Field(default=None)
    trade: Optional[bool] = Field(default=None)
    store: Optional[bool] = Field(default=None)
    cart: Optional[bool] = Field(default=None)
    sell: Optional[bool] = Field(default=None)
    mail: Optional[bool] = Field(default=None)
    auction: Optional[bool] = Field(default=None)
    guildStore: Optional[bool] = Field(default=None)

    # Relações
    rewardForAchievement: Optional[List[str]] = Field(default=None)
    cardPrefix: Optional[str] = Field(default=None)
    pets: Optional[List[str]] = Field(default=None)

    # Listas de relações
    itemSummonInfoContainedIn: Optional[List[ItemSummonInfo]] = Field(default=None)
    sets: Optional[List[ItemSet]] = Field(default=None)
    external_links: Optional[List[str]] = Field(default=None)
    contained_in: Optional[List[ContainedInEntry]] = Field(default=None)
    sold_by: Optional[List[SoldByEntry]] = Field(default=None)
