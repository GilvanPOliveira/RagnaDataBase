from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from passlib.hash import bcrypt
from db.models import User, Inventory
from db.session import get_session
from models.user_model import UserResponse, UserUpdate
from auth.auth_bearer import JWTBearer
from auth.auth_dependencies import admin_required, superadmin_required
from typing import List

router = APIRouter(prefix="/users", tags=["Usuário"])

# Rotas do próprio usuário
@router.get("/me", response_model=UserResponse)
async def get_me(payload=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)):
    user_id = int(payload["sub"])
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
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
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = bcrypt.hash(update_data["password"])
    if "email" in update_data:
        email_query = await db.execute(
            select(User).where(User.email == update_data["email"], User.id != user_id)
        )
        if email_query.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="E-mail já está em uso.")

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
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    await db.execute(delete(Inventory).where(Inventory.user_id == user_id))
    user_email = user.email 
    await db.delete(user)
    await db.commit()
    return {"message": f"Usuário {user_email} deletado com sucesso."}

# Rotas administrativas
@router.get("/", response_model=List[UserResponse], dependencies=[Depends(admin_required)])
async def list_users(db: AsyncSession = Depends(get_session)):
    query = await db.execute(select(User))
    users = query.scalars().all()
    return users

@router.post("/promote/{user_id}", dependencies=[Depends(superadmin_required)])
async def promote_user_to_admin(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user.is_admin:
        raise HTTPException(status_code=400, detail="Usuário já é admin.")
    user.is_admin = True
    await db.commit()
    return {"message": f"Usuário {user.email} promovido a admin."}

@router.delete("/{user_id}", dependencies=[Depends(superadmin_required)], status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    user_email = user.email
    await db.delete(user)
    await db.commit()
    return {"message": f"Usuário {user_email} deletado com sucesso."}

@router.patch("/{user_id}", response_model=UserResponse, dependencies=[Depends(admin_required)])
async def update_user_by_admin(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_session)
): 
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = bcrypt.hash(update_data["password"])
    if "email" in update_data:
        email_query = await db.execute(
            select(User).where(User.email == update_data["email"], User.id != user_id)
        )
        if email_query.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="E-mail já está em uso.")

    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user  
