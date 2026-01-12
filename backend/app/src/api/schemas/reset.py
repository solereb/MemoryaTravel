from pydantic import BaseModel, EmailStr, Field, validator


class EmailSchema(BaseModel):
    email: EmailStr

class TokenSchema(BaseModel):
    token: str = Field(...)

class ResetPasswordSchema(BaseModel):
    token: str = Field(...)
    password: str = Field(..., min_length=8, max_length=15)
    @validator('password')
    def password_complexity_validator(cls, value):
        if not any(c.isdigit() for c in value):
            raise ValueError('Password must contain at least one digit.')
        if not any(c.isalpha() and c.islower() for c in value):
            raise ValueError('Password must contain at least one lowercase Latin letter.')
        if not all(c.islower() or c.isdigit() or c.isupper() for c in value):
            raise ValueError('Password must contain only Latin letters and digits.')
        return value