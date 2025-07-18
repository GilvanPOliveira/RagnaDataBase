import httpx
import re
from models.item_model import (
    ItemModel, ItemSet, ItemSetEntry, SoldByEntry,
    ItemSummonInfo, ContainedInEntry
)
from utils.env_loader import get_env_var

API_KEY = get_env_var("DIVINE_PRIDE_API_KEY")
IMG_JOBS = "https://static.divine-pride.net/images/jobs/icon_jobs_"

ALL_CLASSES_IDS = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20,
    21, 23, 24, 25, 4002, 4003, 4004, 4005, 4006, 4007, 4008, 4009, 4010, 4011,
    4012, 4013, 4015, 4016, 4017, 4018, 4019, 4020, 4021, 4054, 4055, 4056, 4057,
    4058, 4059, 4066, 4067, 4068, 4069, 4070, 4071, 4072, 4190, 4211, 4212, 4215,
    4218, 4239, 4240, 4252, 4253, 4254, 4255, 4256, 4257, 4258, 4259, 4260, 4261,
    4262, 4263, 4264, 4302, 4303, 4304, 4305, 4306, 4307, 4308
]

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

        allowed_raw = data.get("equipJobs")
        allowed_classes = allowed_raw or []

        # Converte string para int quando necessário
        allowed_classes_clean = [
            int(cls_id) if isinstance(cls_id, str) and cls_id.isdigit() else cls_id
            for cls_id in allowed_classes
            if isinstance(cls_id, (int, str))
        ]

        class_icons = [f"{IMG_JOBS}{cls_id}.png" for cls_id in allowed_classes_clean]

        return ItemModel(
            id=data["id"],
            aegisName=data["aegisName"],
            name=data["name"],
            resName=data.get("resName"),
            unidName=data.get("unidName"),
            unidResName=data.get("unidResName"),
            description=strip_colors(data.get("description")),
            unidDescription=strip_colors(data.get("unidDescription")),
            image_icon=f"https://static.divine-pride.net/images/items/item/{item_id}.png",
            image_collection=f"https://static.divine-pride.net/images/items/collection/{item_id}.png",
            slots=data.get("slots"),
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
            weapon_level=data.get("weaponLevel"),
            allowed_classes=allowed_classes_clean,
            class_icons=class_icons
        )
