import uuid
from pydantic import BaseModel, Field, validator, model_validator, ConfigDict
from typing import List
from datetime import date
import uuid

class TravelCreateSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=20)
    date: date
    country_id: int = Field(..., ge=1)
    region_id: int = Field(..., ge=1)
    description: str | None = Field(None, max_length=5000)
    icon_ids: List[int] = Field(default_factory=list, max_items=5)

class TravelResponse(BaseModel):
    id: uuid.UUID
    title: str
    travel_date: date
    country_id: int
    region_id: int
    description: str | None = None
    icon_ids: List[int]
    country_name: str | None = None
    region_name: str | None = None
    media: List[str] | None = None
    model_config = ConfigDict(from_attributes=True)