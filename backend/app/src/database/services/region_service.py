from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.database.models.regions import Region
from src.database.services.errors.coureg_errors import *
from src.core.config import settings
from datetime import datetime, timedelta
import uuid

"""
# src/database/models/region.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import TIMESTAMP, ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from src.database.core.session import Base


class Region(Base):
    __tablename__ = "regions"
    
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    
    country_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("countries.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    name_ru: Mapped[str] = mapped_column(
        String(150), 
        nullable=False, 
        index=True
    )
    
    name_en: Mapped[Optional[str]] = mapped_column(
        String(150), 
        nullable=True
    )
    
    code: Mapped[Optional[str]] = mapped_column(
        String(10), 
        nullable=True,
        index=True
    )
    
    geometry: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True
    )
    
    center_lat: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    
    center_lon: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=func.now(), 
        nullable=False
    )
    
    country: Mapped["Country"] = relationship(
        "Country",
        back_populates="regions"
    )
"""
class RegionService:
    @staticmethod
    async def create(
        session: AsyncSession,
        name_ru: str,
        name_en: str,
        code: str,
        country_id: int
    ) -> Region:
        try:
            region = Region(
                name_ru = name_ru,
                name_en = name_en,
                code = code,
                country_id = country_id
            )
            session.add(region)
            await session.commit()
            await session.refresh(region)
            return region
        except SQLAlchemyError as e:
            await session.rollback()
            raise CouRegServiceError(f'Region service error: {e}')
    
    @staticmethod
    async def get_all_by_country(
        session: AsyncSession,
        country_id: int | None = None,
    ) -> list[Region]:
        q = await session.execute(select(Region).where(Region.country_id == country_id).order_by(Region.name_ru))
        region = q.scalars().all()
        if region:
            return region
        else:
            raise NotFoundCouReg(f'Region not found\\!')
    
    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        region_id: int
    ) -> Region:
        q = await session.execute(select(Region).where(Region.id == region_id))
        region = q.scalar_one_or_none()
        if region:
            return region
        else:
            raise NotFoundCouReg(f'Region not found\\!')