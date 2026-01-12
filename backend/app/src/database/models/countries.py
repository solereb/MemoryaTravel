from datetime import datetime
from sqlalchemy import TIMESTAMP, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from src.database.models.regions import Region
from src.database.core.session import Base

class Country(Base):
    __tablename__ = "countries"
    
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    
    name_ru: Mapped[str] = mapped_column(
        String(150), 
        nullable=False, 
        index=True
    )
    
    name_en: Mapped[str] = mapped_column(
        String(150), 
        nullable=False, 
        index=True
    )
    
    code: Mapped[str] = mapped_column(
        String(2), 
        unique=True, 
        nullable=False, 
        index=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=func.now(), 
        nullable=False
    )
    
    regions: Mapped[list["Region"]] = relationship(
        "Region",
        back_populates="country",
        cascade="all, delete-orphan",
        lazy="selectin"
    )