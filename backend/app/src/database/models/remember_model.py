import uuid
from datetime import datetime, timedelta
from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.database.core.session import Base


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