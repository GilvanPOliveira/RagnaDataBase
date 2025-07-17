from fastapi import APIRouter, Depends, Query
from auth.auth_bearer import JWTBearer
from services.dp_search import search_items_by_name

router = APIRouter(prefix="/search", tags=["Item Name Search"])

@router.get("")
async def search_items(
    name: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    _=Depends(JWTBearer())
):
    all_results = await search_items_by_name(name)

    total = len(all_results)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = all_results[start:end]

    return {"results": paginated, "total": total}
