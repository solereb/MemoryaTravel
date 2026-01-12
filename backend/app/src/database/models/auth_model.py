from sqlalchemy import String, Boolean, TIMESTAMP, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.database.core.session import Base
from datetime import datetime
from typing import List
import uuid


class AuthAccount(Base):
    __tablename__ = "auth_accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_token: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, default=uuid.uuid4)
    verification_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    need_to_be_remembered: Mapped[bool] = mapped_column(Boolean, default=False)
    reset_token: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, onupdate=func.now(), server_default=func.now())

    profile: Mapped["UserProfile"] = relationship(
        back_populates="auth", uselist=False, cascade="all, delete-orphan"
    )
    
    travel: Mapped[List["Travel"]] = relationship(
        back_populates="auth", cascade="all, delete-orphan"
    )
    
    remember_tokens: Mapped[list["RememberToken"]] = relationship(
        back_populates="auth_account", cascade="all, delete-orphan"
    )
    
    tickets: Mapped[List["SupportTicket"]] = relationship(
        back_populates="auth", cascade="all, delete-orphan"
    )