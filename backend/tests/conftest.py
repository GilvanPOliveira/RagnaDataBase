import sys
import os
import warnings

# Ignora todos os DeprecationWarnings vindos do SQLAlchemy
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sqlalchemy")

# Adiciona a raiz do projeto ao sys.path para importações funcionarem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app import app
from db.models import Base
from db.session import get_session

# Usa banco de dados SQLite assíncrono em memória ou disco para testes
DATABASE_URL = "sqlite+aiosqlite:///./test_db.sqlite"
engine = create_async_engine(DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Substitui a dependência get_session do app por esta versão com banco de testes
async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

# Cria o cliente de testes para rodar as requisições com isolamento de banco
@pytest.fixture(scope="module")
async def async_client():
    # Cria as tabelas no banco de testes
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # Limpa o banco após os testes
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
