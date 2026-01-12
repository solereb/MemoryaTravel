import asyncio
from logging.config import fileConfig
import sys
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import engine_from_config
from alembic import context
from src.core.config import settings
from src.database.core.session import Base
from src.database.models.auth_model import AuthAccount
from src.database.models.user_profile import UserProfile
from src.database.models.remember_model import RememberToken
from src.database.models.countries import Country
from src.database.models.regions import Region
from src.database.models.travel import Travel
from src.database.models.tickets import SupportTicket
config = context.config

if config.config_file_name is not None and "alembic" in sys.argv[0]:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

print(f"DEBUG: Количество таблиц в метаданных: {len(target_metadata.tables)}")
print(f"DEBUG: Имена таблиц: {list(target_metadata.tables.keys())}")

# Подставляем URL из settings.py
config.set_main_option(
    "sqlalchemy.url",
    f'postgresql+asyncpg://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_IP}/solereb'
)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    print(config.get_main_option("sqlalchemy.url"),)
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())