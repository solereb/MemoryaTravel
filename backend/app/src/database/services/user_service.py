"""
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth_accounts.id", ondelete="CASCADE"), unique=True, index=True)

    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[Gender | None] = mapped_column(Gender, nullable=True)

    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, onupdate=func.now())

    auth: Mapped["AuthAccount"] = relationship(back_populates="profile")
"""
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database.models.user_profile import UserProfile
from src.database.services.errors.user_errors import *
from src.database.services.region_service import RegionService
import uuid

class UserService:
    @staticmethod
    async def create_user(session: AsyncSession, auth_id: uuid.UUID, username: str) -> UserProfile:
        try:
            user = UserProfile(auth_id=auth_id, username=username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            raise UserServiceError(f'SQLalchemy error: {e}')
        except Exception as e:
            await session.rollback()
            raise UserServiceError(f'SQLalchemy error: {e}')
    
    @staticmethod
    async def get_user(session: AsyncSession, auth_id: uuid.UUID | None = None, username: str | None = None) -> UserProfile:
        try:
            if auth_id:
                q = await session.execute(select(UserProfile).where(UserProfile.auth_id == auth_id))
            if username:
                q = await session.execute(select(UserProfile).where(UserProfile.username == username))
            user = q.scalar_one_or_none()
            return user
        except SQLAlchemyError as e:
            raise UserServiceError(f'SQLalchemy error: {e}')
        except Exception as e:
            raise UserServiceError(f'SQLalchemy error: {e}')
    
    @staticmethod
    async def upgrade_user(session: AsyncSession, auth_id: uuid.UUID | None, gender : str | None = None, age: int | None = None, country_id: int | None = None, region_id: int | None = None):
        try:
            user = await UserService.get_user(session=session, auth_id=auth_id)
            if user is None:
                raise UserNotFoundError(f'User not found')
            if gender:
                user.gender = gender
            if age:
                user.age = age
            if country_id:
                if region_id:
                    region = await RegionService.get_by_id(session=session, region_id=region_id)
                    if region.country_id == country_id:
                        user.country_id = country_id
                        user.region_id = region_id
                    else:
                        raise BadRegion(f'Bad region')
                else:
                    user.country_id = country_id
            user = await session.merge(user)
            await session.commit()
            await session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            raise UserServiceError(f'SQLalchemy error: {e}')
        except Exception as e:
            await session.rollback()
            raise UserServiceError(f'SQLalchemy error: {e}')
    
    @staticmethod
    async def get_all(session: AsyncSession):
        q = await session.execute(select(UserProfile))
        users = q.scalars().all()
        return users