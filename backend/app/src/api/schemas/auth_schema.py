import uuid
from typing import Optional, Union, Dict, Any
from pydantic import BaseModel, Field, validator, EmailStr


class RegistrationSchema(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=5, max_length=20)
    password: str = Field(..., min_length=8, max_length=50)
    @validator('username')
    def username_check(cls, value):
        if not any(c.isalpha() for c in value):
            raise ValueError('Username must contain at least one Latin letter')
        return value
    @validator('password')
    def password_complexity_validator(cls, value):
        if not any(c.isdigit() for c in value):
            raise ValueError('Password must contain at least one digit.')
        if not any(c.isalpha() and c.islower() for c in value):
            raise ValueError('Password must contain at least one lowercase Latin letter.')
        if not all(c.islower() or c.isdigit() or c.isupper() for c in value):
            raise ValueError('Password must contain only Latin letters and digits.')
        return value

class RegistrationSuccessResponse(BaseModel):
    email: str
    username: str
    is_verified: bool
    
    class Config:
        from_attributes = True

class RegistrationErrorResponse(BaseModel):
    detail: str

class VerifyEmailSuccess(BaseModel):
    user_id: uuid.UUID
    email: str
    
    class Config:
        from_attributes = True

class VerifyEmailError(BaseModel):
    detail: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=15)
    remember_me: bool = False

    @validator('password')
    def password_complexity_validator(cls, value):
        if not any(c.isdigit() for c in value):
            raise ValueError('Password must contain at least one digit.')
        if not any(c.isalpha() and c.islower() for c in value):
            raise ValueError('Password must contain at least one lowercase Latin letter.')
        if not all(c.islower() or c.isdigit() or c.isupper() for c in value):
            raise ValueError('Password must contain only Latin letters and digits.')
        return value

class Token(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str = 'bearer'
    
    class Config:
        from_attributes = True

class TokenError(BaseModel):
    detail: str

class RefreshToken(BaseModel):
    refresh_token: str