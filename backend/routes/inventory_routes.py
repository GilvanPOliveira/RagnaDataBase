from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete
from db.models import Inventory, User
from db.session import get_session
from models.inventory_model import (
    InventoryCreate,
    InventoryPublic,
    InventoryUpdate,
    InventoryBatchUpdate
)
from auth.auth_bearer import JWTBearer
from typing import List, Dict

router = APIRouter(prefix="/inventory", tags=["Inventário"])

@router.post("/add")
async def add_to_inventory(
    item: InventoryCreate,
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
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

@router.post("/add_many")
async def add_many_to_inventory(
    items: List[InventoryCreate],
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    added = []
    already = []
    for item in items:
        query = await db.execute(
            select(Inventory).where(
                Inventory.user_id == user_id,
                Inventory.item_id == item.item_id
            )
        )
        existing = query.scalar_one_or_none()
        if existing:
            already.append(item.item_id)
            continue
        new_item = Inventory(
            user_id=user_id,
            item_id=item.item_id,
            item_name=item.item_name,
            image_collection=item.image_collection,
            quantity=item.quantity,
            price=item.price
        )
        db.add(new_item)
        added.append(item.item_id)
    await db.commit()
    return {
        "message": "Operação concluída.",
        "added_item_ids": added,
        "already_in_inventory": already
    }

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

@router.get("/marketplace", response_model=List[InventoryPublic])
async def list_all_marketplace_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_session)
):
    query = await db.execute(
        select(Inventory)
        .options(selectinload(Inventory.user))
        .offset(skip)
        .limit(limit)
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

@router.patch("/update/{item_id}")
async def update_inventory_item(
    item_id: int,
    item_update: InventoryUpdate,
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
        raise HTTPException(status_code=404, detail="Item não encontrado no inventário.")

    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return {"message": "Item atualizado com sucesso."}

@router.delete("/remove_all")
async def remove_all_items(
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    await db.execute(
        delete(Inventory).where(Inventory.user_id == user_id)
    )
    await db.commit()
    return {"message": "Todos os itens do inventário foram removidos com sucesso."}

@router.patch("/update_many")
async def update_many_inventory_items(
    updates: List[InventoryBatchUpdate],
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    updated = []
    for update in updates:
        query = await db.execute(
            select(Inventory).where(
                Inventory.user_id == user_id,
                Inventory.item_id == update.item_id
            )
        )
        item = query.scalar_one_or_none()
        if not item:
            continue
        if update.quantity is not None:
            if update.quantity <= 0:
                await db.delete(item)
                updated.append({"item_id": update.item_id, "action": "deleted"})
                continue
            else:
                item.quantity = update.quantity
        if update.price is not None:
            item.price = update.price
        updated.append({"item_id": update.item_id, "quantity": item.quantity, "price": item.price})
    await db.commit()
    return {"message": "Itens atualizados.", "details": updated}
