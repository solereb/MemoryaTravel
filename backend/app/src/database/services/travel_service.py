from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database.models.travel import Travel
from src.database.services.errors.travel_errors import *
from src.database.services.region_service import RegionService
from datetime import date as date_import
import uuid

class TravelService:
    @staticmethod
    async def create_travel(session: AsyncSession, auth_id: uuid.UUID, title: str, date: date_import, country_id: int, region_id: int, icon_ids: list | None = [], description: str | None = None) -> Travel:
        try:
            travel = Travel(auth_id=auth_id, title=title, travel_date=date, country_id=country_id, region_id=region_id, icon_ids=icon_ids, description=description)
            session.add(travel)
            await session.commit()
            await session.refresh(travel)
            return travel
        except SQLAlchemyError as e:
            await session.rollback()
            raise TravelServiceError(f'SQLalchemy error: {e}')
        except Exception as e:
            await session.rollback()
            raise TravelServiceError(f'SQLalchemy error: {e}')
    
    @staticmethod
    async def get_by_country(session: AsyncSession, auth_id: uuid.UUID, country_id: int) -> list:
        try:
            q = await session.execute(select(Travel).where(Travel.auth_id == auth_id).where(Travel.country_id == country_id))
            travels = q.scalars().all()
            return travels
        except SQLAlchemyError as e:
            raise TravelServiceError(f'SQLalchemy error: {e}')
        except Exception as e:
            raise TravelServiceError(f'SQLalchemy error: {e}')
    
    @staticmethod
    async def get_by_region(session: AsyncSession, auth_id: uuid.UUID, region_id: int) -> list:
        try:
            q = await session.execute(select(Travel).where(Travel.auth_id == auth_id).where(Travel.region_id == region_id))
            travels = q.scalars().all()
            return travels
        except SQLAlchemyError as e:
            raise TravelServiceError(f'SQLalchemy error: {e}')
        except Exception as e:
            raise TravelServiceError(f'SQLalchemy error: {e}')
        
    @staticmethod
    async def get_by_id(session: AsyncSession, travel_id: uuid.UUID | None = None, auth_id: uuid.UUID | None = None) -> Travel:
        try:
            if auth_id:
                q = await session.execute(select(Travel).where(Travel.auth_id == auth_id))
                travels = q.scalars().all()
                return travels
            if travel_id:
                q = await session.execute(select(Travel).where(Travel.id == travel_id))
                travel = q.scalar_one_or_none()
                return travel
        except SQLAlchemyError as e:
            raise TravelServiceError(f'SQLalchemy error: {e}')
        except Exception as e:
            raise TravelServiceError(f'SQLalchemy error: {e}')
    
    @staticmethod
    async def delete(session: AsyncSession, travel_id: uuid.UUID):
        try:
            q = await session.execute(delete(Travel).where(Travel.id == travel_id))
            await session.commit()
            return q.rowcount
        except Exception as e:
            await session.rollback()
            raise TravelServiceError(f'SQLalchemy error: {e}')
    
    @staticmethod
    async def get_all(session: AsyncSession):
        q = await session.execute(select(Travel))
        travels = q.scalars().all()
        return travels