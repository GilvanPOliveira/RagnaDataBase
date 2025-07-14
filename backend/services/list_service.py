from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import List as ListDB, ListItem as ListItemDB, Offer as OfferDB, User as UserDB
from models.list_model import (
    ListItemResponse, SoldBy, LowestUserOffer, DropMonster
)
from sources.manager import get_item_from_sources

async def create_list(db: AsyncSession, user_id: int, name: str) -> ListDB:
    new_list = ListDB(user_id=user_id, name=name)
    db.add(new_list)
    await db.commit()
    await db.refresh(new_list)
    return new_list

async def get_lists(db: AsyncSession, user_id: int) -> List[ListDB]:
    result = await db.execute(select(ListDB).where(ListDB.user_id == user_id))
    return result.scalars().all()

async def add_item_to_list(
    db: AsyncSession, user_id: int, list_id: int, item_id: int, quantity: int
) -> ListItemDB:
    lst = (await db.execute(
        select(ListDB).where(ListDB.id == list_id, ListDB.user_id == user_id)
    )).scalar_one_or_none()
    if not lst:
        raise Exception("Lista não encontrada.")
    new_item = ListItemDB(list_id=list_id, item_id=item_id, quantity=quantity)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

async def update_list_item(
    db: AsyncSession, user_id: int, list_id: int, item_id: int, quantity: int
) -> ListItemDB:
    li = (await db.execute(
        select(ListItemDB)
        .join(ListDB)
        .where(
            ListItemDB.item_id == item_id,
            ListDB.id == list_id,
            ListDB.user_id == user_id
        )
    )).scalar_one_or_none()
    if not li:
        raise Exception("Item não encontrado na lista.")
    li.quantity = quantity
    await db.commit()
    return li

async def remove_list_item(
    db: AsyncSession, user_id: int, list_id: int, item_id: int
):
    li = (await db.execute(
        select(ListItemDB)
        .join(ListDB)
        .where(
            ListItemDB.item_id == item_id,
            ListDB.id == list_id,
            ListDB.user_id == user_id
        )
    )).scalar_one_or_none()
    if not li:
        raise Exception("Item não encontrado na lista.")
    await db.delete(li)
    await db.commit()

async def get_list_items(
    db: AsyncSession, user_id: int, list_id: int
) -> List[ListItemResponse]:
    lst = (await db.execute(
        select(ListDB).where(ListDB.id == list_id, ListDB.user_id == user_id)
    )).scalar_one_or_none()
    if not lst:
        raise Exception("Lista não encontrada.")

    items = (await db.execute(
        select(ListItemDB).where(ListItemDB.list_id == list_id)
    )).scalars().all()

    responses: List[ListItemResponse] = []
    for li in items:
        # 1. Buscar dados do item
        item = await get_item_from_sources(li.item_id)

        # 2. Mapear sold_by (se existir)
        sold_by = []
        if getattr(item, "soldBy", None):
            for e in item.soldBy:
                sold_by.append(SoldBy(
                    npc_name=e.npc_name,
                    map=e.map or "",
                    coordinates=f"{e.x}, {e.y}",
                    price=e.price
                ))

        # 3. Mapear drop_monsters (se existir)
        drop_monsters = []
        if getattr(item, "itemSummonInfoContainedIn", None):
            for e in item.itemSummonInfoContainedIn:
                drop_monsters.append(DropMonster(
                    monster_name=e.targetName,
                    map="",
                    drop_rate=f"{(e.chance or 0)*100:.2f}%",
                    qtd_mob=0
                ))

        # 4. Encontrar menor oferta de usuário
        row = (await db.execute(
            select(OfferDB, UserDB)
            .join(UserDB)
            .where(OfferDB.item_id == li.item_id)
            .order_by(OfferDB.price)
            .limit(1)
        )).first()

        lowest_offer = None
        if row:
            offer, user = row
            lowest_offer = LowestUserOffer(
                price=offer.price,
                user_name=user.name,
                user_email=user.email
            )

        # 5. Montar resposta
        responses.append(ListItemResponse(
            item_id=li.item_id,
            name=item.name,
            image_collection=item.image_collection,
            qtd_item=li.quantity,
            sold_by=sold_by,
            lowest_user_offer=lowest_offer,
            drop_monsters=drop_monsters
        ))
    return responses
