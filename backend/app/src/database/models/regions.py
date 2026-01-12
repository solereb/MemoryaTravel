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
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=func.now(), 
        nullable=False
    )
    
    country: Mapped["Country"] = relationship(
        "Country",
        back_populates="regions"
    )