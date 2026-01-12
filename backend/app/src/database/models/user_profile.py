from sqlalchemy import String, Enum, ForeignKey, TIMESTAMP, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.database.core.session import Base
import uuid
import enum

    
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth_accounts.id", ondelete="CASCADE"), unique=True, index=True)

    username: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(1), nullable=True)
    
    country_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    region_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, onupdate=func.now(), server_default=func.now())

    auth: Mapped["AuthAccount"] = relationship(back_populates="profile")