from fastapi import APIRouter, Depends, Query
from typing import Optional
from auth.auth_bearer import JWTBearer
from auth.auth_dependencies import user_required
from services.dp_search import dp_search_items

router = APIRouter(prefix="/search", tags=["Item Name Search"])

@router.get("")
async def search_items(
    name: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    _=Depends(JWTBearer()),
    __=Depends(user_required)
):
    all_results = await dp_search_items(name)

    total = len(all_results)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = all_results[start:end]

    return {"results": paginated, "total": total}
