import httpx
from bs4 import BeautifulSoup
from models.item_model import ItemModel
import re
 
async def fetch_iro_wiki(item_id: int) -> ItemModel:
    url = f"https://db.irowiki.org/db/item-info/{item_id}/"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

    title = soup.select_one("h1").text.strip() if soup.select_one("h1") else "Unknown"
    desc = soup.select_one("div.content").text.strip() if soup.select_one("div.content") else ""

    text = soup.get_text().lower()

    def extract(pattern):
        match = re.search(pattern, text)
        return match.group(1).strip().title() if match else None

    item_type = extract(r"type:\s*(\w+)")
    item_property = extract(r"property:\s*(\w+)")
    added_date = extract(r"added:\s*(.*?)\\n")

    return ItemModel(
        id=item_id,
        name=title,
        description=desc,
        description_text=desc,
        type=item_type,
        property=item_property,
        added_date=added_date,
        external_links=[url]
    )
