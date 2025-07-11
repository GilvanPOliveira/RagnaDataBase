import asyncio
import asyncpg
from utils.env_loader import get_env_var

DATABASE_URL = get_env_var("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")
RAW_DB_URL = get_env_var("DATABASE_URL")  # para usar com asyncpg puro

async def reset_database():
    conn = await asyncpg.connect(RAW_DB_URL)
    try:
        print("Resetando schema público...")
        await conn.execute("DROP SCHEMA public CASCADE;")
        await conn.execute("CREATE SCHEMA public;")
        print("Banco resetado com sucesso.")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(reset_database())
