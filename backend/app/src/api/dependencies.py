from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.database.core.session import AsyncSessionLocal
from src.core.security import decode_refresh_token, decode_access_token
from src.api.schemas.auth_schema import RefreshToken
from src.api.schemas.reset import TokenSchema
from typing import AsyncGenerator
from src.database.services.auth_service import AuthService
from src.database.services.errors.auth_errors import *
from src.database.services.remember_service import RememberService
from src.database.models.remember_model import RememberToken



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            
async def get_current_refresh_data(
        request: RefreshToken,
        db: AsyncSession = Depends(get_db)
) -> RememberToken | None:
    token = request.refresh_token
    payload = await decode_refresh_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={"WWW-Authenticate": "Bearer"},
        )
    refresh_token = payload.get("token_id")
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token does no contain refresh token',
            headers={"WWW-Authenticate": "Bearer"},
        )
    refresh_data = await RememberService.get(db, refresh_token, None)
    if refresh_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh-token data not found',
            headers={"WWW-Authenticate": "Bearer"},
        )
    if refresh_data.revoked_at != None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh-token has been revoked',
            headers={"WWW-Authenticate": "Bearer"},
        )
    return refresh_data

async def get_current_jwt_data(
    token: str,
    db: AsyncSession
) -> dict | None:
    payload = await decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    reset_token = payload.get('reset_token', None)
    purpose = payload.get('purpose', None)
    if reset_token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    if purpose is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user = await AuthService.get(session=db, reset_token=reset_token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    return user


security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    access_token: str | None = Cookie(None),
    db: AsyncSession = Depends(get_db)
) -> dict | None:
    token = None
    if credentials:
        token = credentials.credentials
    elif access_token:
        token = access_token
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    payload = await decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    user_id = payload.get('user_id')
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    user = await AuthService.get(session=db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User Not Found',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    if user.is_verified == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User Not Activated',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user

async def get_is_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    access_token: str | None = Cookie(None),
    db: AsyncSession = Depends(get_db)
) -> dict | None:
    token = None
    if credentials:
        token = credentials.credentials
    elif access_token:
        token = access_token
    print(credentials)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authenticated',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    payload = await decode_access_token(token)
    print(payload)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    role = payload.get('role')
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    if role == 'admin': return True
    return False