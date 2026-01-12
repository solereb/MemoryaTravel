from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.database.models.remember_model import RememberToken
from src.database.services.errors.remember_errors import *
from src.core.config import settings
from datetime import datetime, timedelta
import uuid

"""
class RememberToken(Base):
    __tablename__ = "remember_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    auth_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("auth_accounts.id", ondelete="CASCADE"),
        nullable=False
    )
    
    token: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)

    revoked_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    auth_account: Mapped["AuthAccount"] = relationship(back_populates="remember_tokens")
"""

class RememberService:
    @staticmethod
    async def create(
        session: AsyncSession,
        token: str,
        auth_acc_id: uuid.UUID,
        expires_at: datetime
    ) -> RememberToken:
        try:
            remember_token = RememberToken(
                token=token,
                auth_account_id=auth_acc_id,
                expires_at=expires_at
            )
            session.add(remember_token)
            await session.commit()
            await session.refresh(remember_token)
            return remember_token
        except SQLAlchemyError as e:
            await session.rollback()
            raise RememberServiceError(f'Remember service error: {e}')
    
    @staticmethod
    async def get(
        session: AsyncSession,
        token: uuid.UUID | None,
        auth_acc_id: uuid.UUID | None
    ) -> RememberToken | None:
        cutoff_date = datetime.utcnow()
        print('In service:')
        print(cutoff_date)
        print(token)
        if token:
            q = await session.execute(select(RememberToken).where(RememberToken.token == token))
        elif auth_acc_id:
            q = await session.execute(select(RememberToken).where(RememberToken.auth_account_id == auth_acc_id))
        else:
            return None
        res = q.scalar_one_or_none()
        print(res)
        return res
    
    @staticmethod
    async def delete(
        session: AsyncSession,
        token: uuid.UUID
    ) -> int:
        try:
            res = await session.execute(delete(RememberToken).where(RememberToken.id == token))
            await session.commit()
            return res.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            raise RememberServiceError(f'Remember service error: {e}')
    
    @staticmethod
    async def revoke(
        session: AsyncSession,
        auth_id: uuid.UUID
    ) -> list[RememberToken]:
        try:
            res = await session.execute(select(RememberToken).where(RememberToken.auth_account_id == auth_id))
            q = res.scalars().all()
            if q:
                for i in q:
                    i.revoked_at = datetime.utcnow()
                    await session.commit()
                    await session.refresh(i)
            return q
        except Exception as e:
            await session.rollback()
            raise RememberServiceError(f'Remember service error: {e}')