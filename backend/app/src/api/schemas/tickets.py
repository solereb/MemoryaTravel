from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import datetime
from enum import Enum

class TicketCategory(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    DATA = "data"
    OTHER = "other"

class TicketPriority(str, Enum):
    LOW = "low"
    HIGH = "high"

class TicketCreate(BaseModel):
    category: str = Field(..., description="Категория обращения")
    priority: str = Field(..., description="Приоритет")
    message: str = Field(..., min_length=1, max_length=2000, description="Текст сообщения")
    @validator('category')
    def category_check(cls, value):
        if not value in ['bug', 'feature', 'data', 'other']:
            raise ValueError('not in buf, feature, data, other')
        return value
    @validator('priority')
    def priority_check(cls, value):
        if not value in ['low', 'high']:
            raise ValueError('not low, high')
        return value
    
class TicketResponse(BaseModel):
    id: UUID
    category: TicketCategory
    priority: TicketPriority
    message: str
    created_at: datetime

    class Config:
        from_attributes = True