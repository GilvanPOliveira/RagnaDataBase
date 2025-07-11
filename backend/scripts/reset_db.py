import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db.session import engine
from db.models import Base

import asyncio

async def reset_database():
    async with engine.begin() as conn:
        # Apagar a tabela de controle do Alembic (resolve o erro!)
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))

        # Apagar todas as tabelas do banco (CASCADE)
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(text(f'DROP TABLE IF EXISTS {table.name} CASCADE'))

        # Recriar tabelas a partir dos modelos
        await conn.run_sync(Base.metadata.create_all)

    print("Banco de dados e Alembic resetados com sucesso!")

if __name__ == "__main__":
    asyncio.run(reset_database())
