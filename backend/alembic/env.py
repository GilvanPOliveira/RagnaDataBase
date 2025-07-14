import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.models import Base
from utils.env_loader import get_env_var

# Carrega configuração do Alembic
config = context.config
DATABASE_URL = get_env_var("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configuração do log
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    """Configura contexto offline (gera SQL sem conexão ativa)"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection):
    """Executa as migrations no banco"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Executa as migrations com conexão assíncrona"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
