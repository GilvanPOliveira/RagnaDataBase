from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import User
from db.session import get_session
from auth.auth_bearer import JWTBearer


async def get_current_user(
    payload=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
):
    user_id = int(payload["sub"])
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    return user


async def admin_required(
    current_user=Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores."
        )
    return current_user


async def superadmin_required(
    current_user=Depends(get_current_user),
):
    if not current_user.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao superadmin."
        )
    return current_user
