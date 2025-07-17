import httpx
from bs4 import BeautifulSoup
from models.item_model import ItemModel, SoldByEntry


async def fetch_dp_html(item_id: int, existing_item: ItemModel) -> ItemModel:
    url = f"https://www.divine-pride.net/database/item/{item_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            return existing_item
        html = resp.text

    soup = BeautifulSoup(html, "html.parser")

    # Nome e Descrição
    h1 = soup.select_one("h1")
    if h1 and not existing_item.name:
        existing_item.name = h1.text.strip()

    description_div = soup.select_one(".item-description")
    if description_div and not existing_item.description:
        existing_item.description = description_div.text.strip()

    # Classes Permitidas (visual icons fallback)
    classes_icons = soup.select(".equiptable img")
    allowed = []
    for img in classes_icons:
        alt = img.attrs.get("alt", "")
        if "off" not in img.attrs.get("src", ""):
            allowed.append(alt)
    if allowed and not existing_item.allowed_classes:
        existing_item.allowed_classes = allowed

    # Campos da Tabela
    fields = {
        "Tipo:": "type",
        "Categoria:": "subtype",
        "Peso:": "weight",
        "Nível da arma:": "weapon_level",
        "Força de Ataque:": "attack",
        "Defesa:": "defense",
        "Slots:": "slots",
        "Nível necessário:": "required_level",
        "Propriedade:": "property",
        "Preço NPC:": "price",
        "Adicionado em:": "added_date",
    }

    for row in soup.select(".item-table tr"):
        th = row.select_one("th")
        td = row.select_one("td")
        if th and td:
            key = th.text.strip()
            value = td.text.strip()
            if key in fields:
                attr = fields[key]
                if attr in ["weight", "attack", "defense", "slots", "weapon_level", "required_level", "price"]:
                    value = int(value.replace(".", "").replace(",", "").split(" ")[0]) if value.replace(".", "").isdigit() else 0
                setattr(existing_item, attr, value)

    # NPC Vendedores
    npcs = []
    for row in soup.select("#sold-by tr"):
        cells = row.select("td")
        if len(cells) >= 3:
            name = cells[0].text.strip() or "Unknown"
            map_name = cells[1].text.strip() or "Unknown"
            price = cells[2].text.strip().replace("z", "").strip()
            price_int = int(price.replace(".", "").replace(",", "")) if price.replace(".", "").isdigit() else 0
            npcs.append(SoldByEntry(npc_name=name, map=map_name, x=0, y=0, price=price_int))
    if npcs and not existing_item.sold_by:
        existing_item.sold_by = npcs

    return existing_item
