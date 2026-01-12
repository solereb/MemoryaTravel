from sqlalchemy import String, Enum, ForeignKey, TIMESTAMP, func, Integer, Date, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.database.core.session import Base
from datetime import date
from typing import List
import uuid
    
class Travel(Base):
    __tablename__ = "travels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth_accounts.id", ondelete="CASCADE"), unique=False, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    travel_date: Mapped[date] = mapped_column(Date, nullable=False)
    
        
    country_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    region_id: Mapped[int | None] = mapped_column(Integer, nullable=False)
    
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon_ids: Mapped[List[int]] = mapped_column(JSON, default=list)
    
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, onupdate=func.now(), server_default=func.now())

    auth: Mapped["AuthAccount"] = relationship(back_populates="travel")