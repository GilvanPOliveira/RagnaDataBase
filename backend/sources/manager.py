from models.item_model import ItemModel
from services.dp_json import fetch_dp_json
from services.dp_html import fetch_dp_html


async def get_item_from_sources(item_id: int) -> ItemModel:
    try:
        item = await fetch_dp_json(item_id)
        item = await fetch_dp_html(item_id, item)
        return item
    except Exception as e:
        raise Exception(f"Erro ao buscar item no Divine Pride: {str(e)}")
