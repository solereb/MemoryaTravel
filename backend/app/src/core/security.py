import bcrypt
from jose import jwt, JWTError
from src.core.config import settings
from datetime import datetime, timedelta
import uuid

async def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def create_access_token(data: dict) -> str:
    """Создание Jwt-токена"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print(expire)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

async def create_refresh_token(remember_me: bool) -> tuple:
    """Создание Refresh-токена"""
    try:
        token_id = uuid.uuid4()
        if remember_me is True:
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.REFRESH_WITHOUT_CHECKED)
        payload = {"token_id": str(token_id), "exp": expire, "type": "refresh"}
        encoded_jwt = jwt.encode(payload, settings.REFRESH_TOKEN_SECRET_KEY, settings.ALGORITHM)
        return (token_id, encoded_jwt, expire)
    except JWTError:
        return None
    
async def decode_access_token(token: str) -> dict | None:
    """Дешифровка Jwt-токена"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        return None

async def decode_refresh_token(token: str) -> dict | None:
    """Дешифровка Refresh-токена"""
    try:
        print(token)
        payload = jwt.decode(token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(payload)
        return payload
    except JWTError as e:
        print(e)
        return None