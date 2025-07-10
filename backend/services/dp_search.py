import httpx
from bs4 import BeautifulSoup
from utils.simple_cache import cache

async def search_items_by_name(name: str) -> list:
    cached = cache.get(name.lower())
    if cached is not None:
        return cached

    url = f"https://www.divine-pride.net/database/search?q={name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        item_rows = soup.select("table.table tbody tr")
        results = []

        for row in item_rows:
            columns = row.find_all("td")
            if len(columns) < 2:
                continue

            item_name = columns[0].get_text(strip=True)
            item_link = columns[0].find("a")
            if not item_link or "/database/item/" not in item_link.get("href", ""):
                continue

            try:
                item_id = int(item_link.get("href").split("/database/item/")[1].split("/")[0])
            except (IndexError, ValueError):
                continue

            if name.lower() in item_name.lower():
                results.append({"id": item_id, "name": item_name})

        cache.set(name.lower(), results)
        return results
