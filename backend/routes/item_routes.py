from fastapi import APIRouter, HTTPException, Query
from services.dp_search import search_items_by_name
from sources.manager import get_item_from_sources
from models.item_model import ItemModel

router = APIRouter(tags=["Item Search"])

@router.get("/item/{item_id}", response_model=ItemModel)
async def get_item(item_id: int):
    try:
        item = await get_item_from_sources(item_id)
        return item
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Item não encontrado. {str(e)}")


@router.get("/search")
async def search_items(
    name: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    try:
        all_results = await search_items_by_name(name)

        start = (page - 1) * per_page
        end = start + per_page
        paginated = all_results[start:end]

        return {
            "total": len(all_results),
            "page": page,
            "per_page": per_page,
            "results": paginated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar item: {str(e)}")
