from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.models import Inventory, User
from db.session import get_session
from models.inventory_model import InventoryCreate, InventoryPublic
from auth.auth_bearer import JWTBearer
from typing import List

router = APIRouter(prefix="/inventory", tags=["Inventário"])


@router.post("/add")
async def add_to_inventory(
    item: InventoryCreate,
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])

    # Verifica se o item já está no inventário do usuário
    query = await db.execute(
        select(Inventory).where(
            Inventory.user_id == user_id,
            Inventory.item_id == item.item_id
        )
    )
    existing = query.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=400, detail="Item já está no inventário.")

    new_item = Inventory(
        user_id=user_id,
        item_id=item.item_id,
        item_name=item.item_name,
        image_collection=item.image_collection,
        quantity=item.quantity,
        price=item.price
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return {"message": "Item adicionado ao inventário."}


@router.get("/list", response_model=List[InventoryPublic])
async def list_inventory(
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])

    query = await db.execute(
        select(Inventory)
        .options(selectinload(Inventory.user))
        .where(Inventory.user_id == user_id)
    )
    items = query.scalars().all()

    results = []
    for inv in items:
        results.append(InventoryPublic(
            item_id=inv.item_id,
            item_name=inv.item_name,
            image_collection=inv.image_collection,
            quantity=inv.quantity,
            price=inv.price,
            user={
                "id": inv.user.id,
                "email": inv.user.email,
                "name": inv.user.name
            }
        ))

    return results


@router.get("/marketplace/{item_id}", response_model=List[InventoryPublic])
async def list_item_for_marketplace(item_id: int, db: AsyncSession = Depends(get_session)):
    query = await db.execute(
        select(Inventory)
        .options(selectinload(Inventory.user))
        .where(Inventory.item_id == item_id)
    )
    items = query.scalars().all()

    if not items:
        raise HTTPException(
            status_code=404, detail="Nenhum usuário possui este item à venda.")

    results = []
    for inv in items:
        results.append(InventoryPublic(
            item_id=inv.item_id,
            item_name=inv.item_name,
            image_collection=inv.image_collection,
            quantity=inv.quantity,
            price=inv.price,
            user={
                "id": inv.user.id,
                "email": inv.user.email,
                "name": inv.user.name
            }
        ))

    return results


@router.delete("/remove/{item_id}")
async def remove_item(
    item_id: int,
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])

    query = await db.execute(
        select(Inventory).where(
            Inventory.user_id == user_id,
            Inventory.item_id == item_id
        )
    )
    item = query.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=404, detail="Item não encontrado no inventário.")

    await db.delete(item)
    await db.commit()

    return {"message": "Item removido do inventário."}
