import httpx
import re
from models.item_model import ItemModel, ItemSet, ItemSetEntry, SoldByEntry, ItemSummonInfo, ContainedInEntry
from utils.env_loader import get_env_var

API_KEY = get_env_var("DIVINE_PRIDE_API_KEY")

def strip_colors(text: str) -> str:
    if not text:
        return None
    return re.sub(r"\^(?:[0-9a-fA-F]{6})", "", text).replace("\n", " ").strip()

async def fetch_dp_json(item_id: int) -> ItemModel:
    url = f"https://www.divine-pride.net/api/database/Item/{item_id}?apiKey={API_KEY}&server=bRO"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()

        return ItemModel(
            id=data["id"],
            aegisName=data["aegisName"],
            name=data["name"],
            resName=data.get("resName"),
            unidName=data.get("unidName"),
            unidResName=data.get("unidResName"),
            description=data.get("description"),
            unidDescription=strip_colors(data.get("unidDescription")),
            description_text=strip_colors(data.get("description")),
            image_icon=f"https://static.divine-pride.net/images/items/item/{item_id}.png",
            image_collection=f"https://static.divine-pride.net/images/items/collection/{item_id}.png",
            slots=data.get("slots"),
            itemLevel=data.get("itemLevel"),
            itemTypeId=data.get("itemTypeId"),
            itemSubTypeId=data.get("itemSubTypeId"),
            attack=data.get("attack"),
            matk=data.get("matk"),
            defense=data.get("defense"),
            weight=data.get("weight"),
            requiredLevel=data.get("requiredLevel"),
            refinable=data.get("refinable"),
            indestructible=data.get("indestructible"),
            gender=data.get("gender"),
            range=data.get("range"),
            attribute=data.get("attribute"),
            price=data.get("price"),
            location=data.get("location"),
            compositionPos=data.get("compositionPos"),
            EQUIP=data.get("EQUIP"),
            LOCA=data.get("LOCA"),
            hasScript=data.get("hasScript"),
            pets=data.get("pets", []),
            cardPrefix=data.get("cardPrefix"),
            rewardForAchievement=data.get("rewardForAchievement", []),
            itemSummonInfoContainedIn=[
                ItemSummonInfo(
                    sourceId=e["sourceId"],
                    sourceName=e["sourceName"],
                    targetId=e["targetId"],
                    targetName=e["targetName"],
                    chance=e.get("chance", 0) / 100
                )
                for e in data.get("itemSummonInfoContainedIn", [])
            ] or None,
            contained_in=[
                ContainedInEntry(
                    source_name=e["sourceName"],
                    chance=e.get("chance", 0) / 100
                )
                for e in data.get("itemSummonInfoContainedIn", [])
            ] or None,
            sets=[
                ItemSet(
                    name=s["name"],
                    items=[
                        ItemSetEntry(itemId=i["itemId"], name=i["name"]) for i in s.get("items", [])
                    ]
                )
                for s in data.get("sets", [])
            ] or None,
            sold_by=[
                SoldByEntry(
                    npc_name=e["npc"]["name"],
                    map=e["npc"].get("map") or "Unknown",
                    x=e["npc"].get("x", 0),
                    y=e["npc"].get("y", 0),
                    price=e["price"]
                )
                for e in data.get("soldBy", []) if e.get("npc")
            ] or None,
            external_links=[
                f"http://db.irowiki.org/db/item-info/{item_id}/",
                f"https://kafra.kr/#!/en/KRO/itemdetail/{item_id}"
            ],
            usable_by=strip_colors(data.get("description")).split("Usable By:")[-1].strip() if "Usable By:" in data.get("description", "") else None,
            weapon_level=int(re.search(r"Weapon Level: \^808080(\d+)", data.get("description", "")).group(1)) if "Weapon Level:" in data.get("description", "") else None
        )
