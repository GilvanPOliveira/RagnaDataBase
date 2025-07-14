from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from db.models import List as ListModel, ListItem as ListItemModel
from db.session import get_session
from models.list_model import (
    ListCreate, ListRead,
    BulkListItemCreate, UpdateListItem,
    ListItemResponse, SoldBy, LowestUserOffer, DropMonster
)
from auth.auth_dependencies import get_current_user
from sources.manager import get_item_from_sources

router = APIRouter(prefix="/lists", tags=["lists"])

@router.post("/", response_model=ListRead, status_code=status.HTTP_201_CREATED)
async def create_list(
    data: ListCreate,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # Gera local_id incremental POR USUÁRIO
    max_local = await db.scalar(
        select(func.max(ListModel.local_id)).where(ListModel.user_id == current_user.id)
    )
    local_id = (max_local or 0) + 1

    nova = ListModel(user_id=current_user.id, name=data.name, local_id=local_id)
    db.add(nova)
    await db.commit()
    await db.refresh(nova)

    # Retorne o modelo Pydantic preenchido manualmente
    return ListRead(
        id=nova.id,
        local_id=nova.local_id,
        name=nova.name,
        created_at=nova.created_at,
        updated_at=nova.updated_at,
        items=[]
    )

@router.get("/", response_model=List[ListRead])
async def get_lists(
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    q = await db.execute(
        select(ListModel).where(ListModel.user_id == current_user.id)
    )
    listas = q.scalars().all()
    output: List[ListRead] = []

    for lst in listas:
        # Busca itens brutos
        q2 = await db.execute(
            select(ListItemModel).where(ListItemModel.list_id == lst.id)
        )
        raw_items = q2.scalars().all()

        enriched: List[ListItemResponse] = []
        for li in raw_items:
            info = await get_item_from_sources(li.item_id)

            sold_by = [
                SoldBy(
                    npc_name=e.npc_name,
                    map=e.map or "",
                    coordinates=f"{e.x},{e.y}",
                    price=e.price
                )
                for e in getattr(info, "soldBy", []) or []
            ]
            drop_monsters = [
                DropMonster(
                    monster_name=getattr(e, "targetName", ""),
                    map="",
                    drop_rate=f"{(getattr(e, 'chance', 0) or 0)*100:.2f}%",
                    qtd_mob=0
                )
                for e in getattr(info, "itemSummonInfoContainedIn", []) or []
            ]
            # menor oferta de usuário
            row = (await db.execute(
                select(db.models.Offer, db.models.User)
                .join(db.models.User)
                .where(db.models.Offer.item_id == li.item_id)
                .order_by(db.models.Offer.price)
                .limit(1)
            )).first()
            lowest = None
            if row:
                offer, user = row
                lowest = LowestUserOffer(
                    price=offer.price,
                    user_name=user.name,
                    user_email=user.email
                )

            enriched.append(ListItemResponse(
                item_id=li.item_id,
                name=info.name,
                image_collection=info.image_collection,
                qtd_item=li.quantity,
                sold_by=sold_by,
                lowest_user_offer=lowest,
                drop_monsters=drop_monsters
            ))

        output.append(ListRead(
            id=lst.id,
            local_id=lst.local_id,
            name=lst.name,
            created_at=lst.created_at,
            updated_at=lst.updated_at,
            items=enriched
        ))

    return output

@router.post(
    "/{list_id}/items",
    response_model=List[ListItemResponse],
    status_code=status.HTTP_201_CREATED
)
async def add_items(
    list_id: int,
    payload: BulkListItemCreate,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    q = await db.execute(
        select(ListModel)
        .where(ListModel.id == list_id, ListModel.user_id == current_user.id)
    )
    if not q.scalar_one_or_none():
        raise HTTPException(404, "Lista não encontrada")

    objs = [
        ListItemModel(list_id=list_id, item_id=i.item_id, quantity=i.quantity)
        for i in payload.items
    ]
    db.add_all(objs)
    await db.commit()

    enriched = []
    for li in objs:
        info = await get_item_from_sources(li.item_id)
        sold_by = [
            SoldBy(
                npc_name=e.npc_name,
                map=e.map or "",
                coordinates=f"{e.x},{e.y}",
                price=e.price
            )
            for e in getattr(info, "soldBy", []) or []
        ]
        drop_monsters = [
            DropMonster(
                monster_name=getattr(e, "targetName", ""),
                map="",
                drop_rate=f"{(getattr(e, 'chance', 0) or 0)*100:.2f}%",
                qtd_mob=0
            )
            for e in getattr(info, "itemSummonInfoContainedIn", []) or []
        ]
        enriched.append(
            ListItemResponse(
                item_id=li.item_id,
                name=info.name,
                image_collection=info.image_collection,
                qtd_item=li.quantity,
                sold_by=sold_by,
                lowest_user_offer=None,
                drop_monsters=drop_monsters
            )
        )
    return enriched

@router.put(
    "/{list_id}/items",
    response_model=List[ListItemResponse],
    status_code=status.HTTP_200_OK
)
async def update_items_bulk(
    list_id: int,
    payload: BulkListItemCreate,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # valida lista pertence ao usuário
    q = await db.execute(
        select(ListModel)
        .where(ListModel.id == list_id, ListModel.user_id == current_user.id)
    )
    if not q.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    updated_objs: List[ListItemModel] = []
    # atualiza cada item enviado
    for itm in payload.items:
        li = (await db.execute(
            select(ListItemModel)
            .where(
                ListItemModel.list_id == list_id,
                ListItemModel.item_id == itm.item_id
            )
        )).scalar_one_or_none()
        if not li:
            raise HTTPException(
                status_code=404,
                detail=f"Item {itm.item_id} não encontrado na lista"
            )
        li.quantity = itm.quantity
        updated_objs.append(li)

    await db.commit()

    # monta a resposta enriquecida
    enriched: List[ListItemResponse] = []
    for li in updated_objs:
        info = await get_item_from_sources(li.item_id)

        sold = [
            SoldBy(
                npc_name=e.npc_name,
                map=e.map or "",
                coordinates=f"{e.x},{e.y}",
                price=e.price
            )
            for e in getattr(info, "soldBy", []) or []
        ]
        drops = [
            DropMonster(
                monster_name=getattr(e, "targetName", ""),
                map="",
                drop_rate=f"{(getattr(e, 'chance', 0) or 0)*100:.2f}%",
                qtd_mob=0
            )
            for e in getattr(info, "itemSummonInfoContainedIn", []) or []
        ]

        enriched.append(ListItemResponse(
            item_id=li.item_id,
            name=info.name,
            image_collection=info.image_collection,
            qtd_item=li.quantity,
            sold_by=sold,
            lowest_user_offer=None,
            drop_monsters=drops
        ))

    return enriched

@router.delete(
    "/{list_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_item(
    list_id: int,
    item_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    q = await db.execute(
        select(ListItemModel)
        .join(ListModel)
        .where(
            ListItemModel.item_id == item_id,
            ListModel.id == list_id,
            ListModel.user_id == current_user.id
        )
    )
    li = q.scalar_one_or_none()
    if not li:
        raise HTTPException(404, "Item não encontrado na lista")

    await db.delete(li)
    await db.commit()

@router.get(
    "/{list_id}/items",
    response_model=List[ListItemResponse],
    status_code=status.HTTP_200_OK
)
async def get_list_items(
    list_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # Verifica se a lista existe e pertence ao usuário
    q = await db.execute(
        select(ListModel)
        .where(ListModel.id == list_id, ListModel.user_id == current_user.id)
    )
    lst = q.scalar_one_or_none()
    if not lst:
        raise HTTPException(404, "Lista não encontrada")

    # Busca os itens da lista
    q2 = await db.execute(
        select(ListItemModel).where(ListItemModel.list_id == list_id)
    )
    raw_items = q2.scalars().all()

    enriched: List[ListItemResponse] = []
    for li in raw_items:
        info = await get_item_from_sources(li.item_id)

        sold_by = [
            SoldBy(
                npc_name=e.npc_name,
                map=e.map or "",
                coordinates=f"{e.x},{e.y}",
                price=e.price
            )
            for e in getattr(info, "soldBy", []) or []
        ]
        drop_monsters = [
            DropMonster(
                monster_name=getattr(e, "targetName", ""),
                map="",
                drop_rate=f"{(getattr(e, 'chance', 0) or 0)*100:.2f}%",
                qtd_mob=0
            )
            for e in getattr(info, "itemSummonInfoContainedIn", []) or []
        ]

        enriched.append(ListItemResponse(
            item_id=li.item_id,
            name=info.name,
            image_collection=info.image_collection,
            qtd_item=li.quantity,
            sold_by=sold_by,
            lowest_user_offer=None,
            drop_monsters=drop_monsters
        ))

    return enriched
