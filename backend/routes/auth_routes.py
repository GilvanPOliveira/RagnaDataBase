from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import bcrypt
from db.models import User
from db.session import get_session
from models.user_model import UserCreate, UserLogin, UserResponse, TokenResponse
from auth.auth_handler import create_access_token
from auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    query = await db.execute(select(User).where(User.email == user.email))
    existing_user = query.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    hashed_password = bcrypt.hash(user.password)
    new_user = User(email=user.email, password=hashed_password, name=user.name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_session)):
    query = await db.execute(select(User).where(User.email == user.email))
    db_user = query.scalar_one_or_none()
    if not db_user or not bcrypt.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token}

@router.get("/me", response_model=UserResponse)
async def get_me(payload=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)):
    user_id = int(payload["sub"])
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user
