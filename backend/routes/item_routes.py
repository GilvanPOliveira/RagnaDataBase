from fastapi import APIRouter, HTTPException
from sources.manager import get_item_from_sources
from models.item_model import ItemModel

router = APIRouter()

@router.get("/item/{item_id}", response_model=ItemModel)
async def get_item(item_id: int):
    try:
        item = await get_item_from_sources(item_id)
        return item
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
