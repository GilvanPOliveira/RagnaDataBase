from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from passlib.hash import bcrypt
from typing import List

from models.user_model import AdminUpdate
from db.models import User, Inventory
from db.session import get_session
from models.user_model import UserResponse, UserUpdate
from auth.auth_bearer import JWTBearer
from auth.auth_dependencies import admin_required, superadmin_required

router = APIRouter(prefix="/users", tags=["Usuário"])

# Rotas do próprio usuário

@router.get("/me", response_model=UserResponse)
async def get_me(
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user 

@router.patch("/me", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = bcrypt.hash(update_data["password"])
    if "email" in update_data:
        # verifica se já existe outro com o mesmo e‑mail
        email_q = await db.execute(
            select(User).where(User.email == update_data["email"], User.id != user_id)
        )
        if email_q.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="E‑mail já está em uso.")

    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user  

@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_me(
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # limpa inventário antes de remover
    await db.execute(delete(Inventory).where(Inventory.user_id == user_id))
    user_email = user.email 
    await db.delete(user)
    await db.commit()
    return {"message": f"Usuário {user_email} deletado com sucesso."}


# Rotas administrativas

@router.get(
    "/",
    response_model=List[UserResponse],
    dependencies=[Depends(admin_required)]
)
async def list_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.patch(
    "/{user_id}/admin",
    dependencies=[Depends(superadmin_required)]
)
async def set_admin_status(
    user_id: int,
    admin_update: AdminUpdate,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user.is_admin == admin_update.is_admin:
        status_msg = "já é admin" if admin_update.is_admin else "já não é admin"
        raise HTTPException(status_code=400, detail=f"Usuário {status_msg}.")
    user.is_admin = admin_update.is_admin
    await db.commit()
    await db.refresh(user)
    action = "promovido a admin" if user.is_admin else "removido de admin"
    return {"message": f"Usuário {user.email} {action} com sucesso."}

@router.delete(
    "/{user_id}",
    dependencies=[Depends(superadmin_required)],
    status_code=status.HTTP_200_OK
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    user_email = user.email
    await db.delete(user)
    await db.commit()
    return {"message": f"Usuário {user_email} deletado com sucesso."}

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(admin_required)]
)
async def update_user_by_admin(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = bcrypt.hash(update_data["password"])
    if "email" in update_data:
        email_q = await db.execute(
            select(User).where(User.email == update_data["email"], User.id != user_id)
        )
        if email_q.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="E‑mail já está em uso.")

    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user  
