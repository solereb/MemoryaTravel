import uuid
from typing import Optional, Union, Dict, Any
from pydantic import BaseModel, Field, validator, EmailStr, model_validator


class UserUpdateSchema(BaseModel):
    age: int | None = Field(ge=6, le=100)
    gender: str | None = Field()
    country_id: int | None = Field()
    region_id: int | None = Field()
    @model_validator(mode='after')
    def check_at_least_one(cls, values):
        filled = [v for v in values.dict().values() if v is not None]
        data = values.model_dump()
        if len(filled) == 0:
            raise ValueError('Minimum one field required')
        if data.get('region_id') is not None and data.get('country_id') is None:
            raise ValueError('You need to provide country_id if you update region_id')
        return values
    @validator('gender')
    def gender_check(cls, value):
        if value:
            if value not in ('M', 'F'):
                raise ValueError('Gender can be only male or female')
        return value

    class Config:
        from_attributes = True

class UserUpdateResponse(BaseModel):
    age: int | None = None
    gender: str | None = None
    country_id: int | None = None
    region_id: int | None = None

class ProfileGetResponse(BaseModel):
    email: EmailStr
    username: str
    age: int | None
    gender: str | None
    country_id: int | None
    country_name: str | None
    region_id: int | None
    region_name: str | None