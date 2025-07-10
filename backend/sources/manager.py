from models.item_model import ItemModel
from services.dp_json import fetch_dp_json
from services.dp_html import fetch_dp_html
from services.iro_wiki import fetch_iro_wiki
from services.ragna_api import fetch_ragna_api

async def get_item_from_sources(item_id: int) -> ItemModel:
    errors = []

    try:
        base = await fetch_dp_json(item_id)
    except Exception as e:
        errors.append(f"DP JSON failed: {str(e)}")
        base = None

    if base:
        # Tentativa de completar com dados ausentes
        for fallback in [fetch_dp_html, fetch_iro_wiki, fetch_ragna_api]:
            try:
                extra = await fallback(item_id)
                for field in ItemModel.model_fields:
                    val = getattr(base, field)
                    fallback_val = getattr(extra, field)
                    if val in (None, [], "", 0) and fallback_val not in (None, [], "", 0):
                        setattr(base, field, fallback_val)
                break
            except Exception as e:
                errors.append(f"{fallback.__name__} failed: {str(e)}")
        return base

    # Se nem o JSON funcionou, tenta os outros diretamente
    for fallback in [fetch_dp_html, fetch_iro_wiki, fetch_ragna_api]:
        try:
            return await fallback(item_id)
        except Exception as e:
            errors.append(f"{fallback.__name__} failed: {str(e)}")

    raise Exception("Todas as fontes falharam:\n" + "\n".join(errors))
