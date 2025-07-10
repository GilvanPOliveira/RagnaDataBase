from models.item_model import ItemModel
from services.dp_json import fetch_dp_json

async def get_item_from_sources(item_id: int) -> ItemModel:
    try:
        return await fetch_dp_json(item_id)
    except Exception as e:
        raise Exception(f"Erro ao buscar item no Divine Pride: {str(e)}")
