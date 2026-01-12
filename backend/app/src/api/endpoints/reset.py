from fastapi import APIRouter, status, Depends, HTTPException, Response

from src.api.dependencies import get_db, get_current_jwt_data
from src.database.services.auth_service import AuthService
from src.database.services.remember_service import RememberService
from src.database.services.errors.auth_errors import *
from src.database.services.errors.remember_errors import *
from src.core.security import (
    hash_password, 
    create_access_token,
    verify_password
)
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from src.utils.email import send_email_reset
from src.api.schemas.reset import EmailSchema, TokenSchema, ResetPasswordSchema
import asyncio


router = APIRouter(prefix='/reset', tags=['Reset'])


@router.post(
    '/forgot_password',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Send email with token',
    description='Sending email with url to reset the password'
)
async def send_reset_email(content: EmailSchema, session: AsyncSession = Depends(get_db)):
    email = content.email
    auth = await AuthService.update_reset(session=session, email=email)
    if auth is not None:
        data = {"reset_token": str(auth.reset_token), "purpose": "reset"}
        token = await create_access_token(data)
        url = f'http://127.0.0.1/reset_password.html?token={token}'
        print(url)
        asyncio.create_task(send_email_reset(email, url))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get(
    '/from_email',
    response_model=None,
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Check reset token',
    description='Check reset token and if answer is 200 frontend can show form'
)
async def check_token(data: TokenSchema = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_current_jwt_data(data.token, db)
    if user:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
@router.post(
    '/reset_password',
    response_model=None,
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Reset password',
    description='Reset user password using JWT reset token'
)
async def reset_password(data: ResetPasswordSchema, db: AsyncSession = Depends(get_db)):
    user = await get_current_jwt_data(data.token, db)
    password_hash = await hash_password(data.password)
    if await verify_password(data.password, user.password_hash) is True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password need to be different from the last one')
    await AuthService.update_password(session=db, user_id=user.id, password_hash=password_hash)
    await AuthService.update_reset(session=db, user_id=user.id)
    await RememberService.revoke(session=db, auth_id=user.id)
    return Response(status_code=status.HTTP_200_OK)

