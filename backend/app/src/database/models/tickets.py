import uuid
import enum
from sqlalchemy import String, Enum, ForeignKey, TIMESTAMP, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.database.core.session import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    auth_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth_accounts.id", ondelete="CASCADE"), index=True)
    category: Mapped[str] = mapped_column(String(10), nullable=False)
    priority: Mapped[str] = mapped_column(String(10), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    auth: Mapped["AuthAccount"] = relationship(back_populates="tickets")