from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.database.models.tickets import SupportTicket
from src.database.services.errors.remember_errors import *
from src.core.config import settings
from datetime import datetime, timedelta
import uuid

"""
import uuid
import enum
from sqlalchemy import String, Enum, ForeignKey, TIMESTAMP, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.database.core.session import Base

class TicketCategory(enum.Enum):
    BUG = "bug"
    FEATURE = "feature"
    DATA = "data"
    OTHER = "other"

class TicketPriority(enum.Enum):
    LOW = "low"
    HIGH = "high"

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    auth_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth_accounts.id", ondelete="CASCADE"), unique=True, index=True)
    category: Mapped[TicketCategory] = mapped_column(Enum(TicketCategory), nullable=False, default=TicketCategory.OTHER)
    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority), nullable=False, default=TicketPriority.LOW)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    auth: Mapped["AuthAccount"] = relationship(back_populates="tickets")
"""

class TicketService:
    @staticmethod
    async def create(
        session: AsyncSession,
        auth_id: uuid.UUID,
        category: str,
        priority: str,
        message: str
    ) -> SupportTicket:
        try:
            ticket = SupportTicket(
                auth_id = auth_id,
                category= category,
                priority=priority,
                message=message
            )
            session.add(ticket)
            await session.commit()
            await session.refresh(ticket)
            return ticket
        except SQLAlchemyError as e:
            print(e)
            await session.rollback()
            return None
    
    @staticmethod
    async def get(
        session: AsyncSession,
        ticket_id: uuid.UUID
    ) -> SupportTicket | None:
        cutoff_date = datetime.utcnow()
        q = await session.execute(select(SupportTicket).where(SupportTicket.id == ticket_id))
        res = q.scalar_one_or_none()
        return res
    
    @staticmethod
    async def delete(
        session: AsyncSession,
        ticket_id: uuid.UUID
    ) -> int:
        try:
            res = await session.execute(delete(SupportTicket).where(SupportTicket.id == ticket_id))
            await session.commit()
            return res.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            return None
    
    @staticmethod
    async def get_all(
        session: AsyncSession
    ):
        q = await session.execute(select(SupportTicket))
        res = q.scalars().all()
        return res