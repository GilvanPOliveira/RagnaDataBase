import httpx
from bs4 import BeautifulSoup
from models.item_model import ItemModel, SoldByEntry
import re
 
async def fetch_dp_html(item_id: int) -> ItemModel:
    url = f"https://www.divine-pride.net/database/item/{item_id}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

    title = soup.select_one("h2").text.strip() if soup.select_one("h2") else "Unknown"
    description = soup.select_one(".dp-content").text.strip() if soup.select_one(".dp-content") else ""

    sold_by = []
    sold_table = soup.find("table", {"id": "table-npc-buy"})
    if sold_table:
        for row in sold_table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 5:
                npc_name = cols[0].text.strip()
                map_name = cols[1].text.strip()
                x = int(cols[2].text.strip())
                y = int(cols[3].text.strip())
                price = int(cols[4].text.strip().replace(",", ""))
                sold_by.append(SoldByEntry(
                    npc_name=npc_name,
                    map=map_name,
                    x=x,
                    y=y,
                    price=price
                ))

    return ItemModel(
        id=item_id,
        name=title,
        description=description,
        description_text=description,
        sold_by=sold_by or None,
        external_links=[
            f"https://www.divine-pride.net/database/item/{item_id}"
        ]
    )
