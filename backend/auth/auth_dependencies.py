from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import User
from db.session import get_session
from auth.auth_bearer import JWTBearer

async def admin_required(
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores.")
    return user

async def superadmin_required(
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user or not user.is_superadmin:
        raise HTTPException(status_code=403, detail="Acesso restrito ao superadmin.")
    return user
