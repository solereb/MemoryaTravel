from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.database.models.countries import Country
from src.database.services.errors.coureg_errors import *
from src.core.config import settings
from datetime import datetime, timedelta
import uuid

"""
from datetime import datetime
from sqlalchemy import TIMESTAMP, ForeignKey, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from typing import Optional, List, Dict, Any
from src.database.core.session import Base


class Country(Base):
    __tablename__ = "countries"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    name_ru: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    
    name_en: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    
    code: Mapped[str] = mapped_column(String(2), unique=True, nullable=False, index=True)
    
    regions: Mapped[List["Region"]] = relationship(
        back_populates="country", 
        cascade="all, delete-orphan"
    )
"""
class CountryService:
    @staticmethod
    async def create(
        session: AsyncSession,
        name_ru: str,
        name_en: str,
        code: str,
    ) -> Country:
        try:
            country = Country(
                name_ru = name_ru,
                name_en = name_en,
                code = code
            )
            session.add(country)
            await session.commit()
            await session.refresh(country)
            return country
        except SQLAlchemyError as e:
            await session.rollback()
            raise CouRegServiceError(f'Country service error: {e}')
    
    @staticmethod
    async def get(
        session: AsyncSession,
        country_id: int | None = None,
        code: str | None = None
    ) -> Country:
        cutoff_date = datetime.utcnow()
        if country_id:
            q = await session.execute(select(Country).where(Country.id == country_id))
        elif code:
            q = await session.execute(select(Country).where(Country.code == code))
        else:
            return None
        country = q.scalar_one_or_none()
        if country:
            return country
        else:
            raise NotFoundCouReg(f'Country not found\\!')
    
    @staticmethod
    async def get_all(
        session: AsyncSession
    ) -> list[Country]:
        q = await session.execute(select(Country).order_by(Country.name_ru))
        return q.scalars().all()