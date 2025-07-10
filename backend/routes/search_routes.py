from fastapi import APIRouter, Query
from services.dp_search import search_items_by_name

router = APIRouter()

@router.get("/search")
async def search_items(name: str, page: int = 1, per_page: int = 10):
    try:
        all_results = await search_items_by_name(name)
        total = len(all_results)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_results = all_results[start:end]
        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "results": paginated_results
        }
    except Exception as e:
        return {"detail": str(e)}
