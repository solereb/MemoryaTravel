from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.core.config import settings


DATABASE_URL = f'postgresql+asyncpg://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_IP}/solereb'

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def create_tables():
    """Функция создания таблиц postgresql"""
    from src.database.models.auth_model import AuthAccount
    from src.database.models.user_profile import UserProfile
    from src.database.models.remember_model import RememberToken
    from src.database.models.countries import Country
    from src.database.models.regions import Region
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)