import httpx
from models.item_model import ItemModel

async def fetch_ragna_api(item_id: int) -> ItemModel:
    url = f"https://www.ragnaapi.com/api/v1/items/{item_id}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

    return ItemModel(
        id=data.get("id", item_id),
        name=data.get("name", "Unknown"),
        description=data.get("description"),
        description_text=data.get("description"),
        image_icon=data.get("icon"),
        external_links=[url]
    )
 