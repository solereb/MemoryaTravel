from fastapi import APIRouter, status, Depends, HTTPException, Response
from src.api.schemas.auth_schema import (
    RegistrationErrorResponse, 
    RegistrationSchema, 
    RegistrationSuccessResponse,
    VerifyEmailError,
    VerifyEmailSuccess,
    LoginSchema,
    Token,
    RefreshToken,
    TokenError
)
from src.api.dependencies import get_db, get_current_refresh_data
from src.database.services.auth_service import AuthService
from src.database.services.remember_service import RememberService
from src.database.services.user_service import UserService
from src.database.services.errors.auth_errors import *
from src.database.services.errors.remember_errors import *
from src.database.services.errors.user_errors import *
from src.core.security import (
    hash_password, 
    verify_password,
    create_access_token,
    create_refresh_token
)
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from src.utils.email import send_email_verification
import asyncio
from src.core.config import settings


router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/registration',
    response_model=RegistrationSuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": RegistrationErrorResponse},
        500: {"description": "Internal server error"}
    },
    summary='Registration',
    description='Create a new user using email, password and bool for refresh-token remembering'
)
async def register_user(content: RegistrationSchema, db: AsyncSession = Depends(get_db)) -> RegistrationSuccessResponse:
    hashed_password = await hash_password(content.password)
    
    try:
        auth_cont = await AuthService.create(
            session=db, 
            email=content.email, 
            password_hash=hashed_password
        )
        asyncio.create_task(send_email_verification(content.email, f'http://127.0.0.12/verify.html?token={auth_cont.verification_token}'))
        print(f'http://127.0.0.1:5500/verify.html?token={auth_cont.verification_token}')
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already exist'
        )
    user = await UserService.create_user(session=db, auth_id=auth_cont.id, username=content.username)
    return RegistrationSuccessResponse(
        username=user.username,
        email=auth_cont.email,
        is_verified=auth_cont.is_verified
    )

@router.get(
    '/email/verify/{token}',
    response_model=VerifyEmailSuccess,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": VerifyEmailError},
        500: {"detail": "Internal server error"}
    },
    summary="Email Verify",
    description="Verify email using uuid4 token (lifetime is 24 hours)"
    )
async def verify_email(token: str, db: AsyncSession = Depends(get_db)) -> VerifyEmailSuccess:
    try:
        auth_data = await AuthService.verify_email(db, uuid.UUID(token))
    except AccountNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Account not found'
        )
    except IsAlreadyVerified as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email is already verified'
        )
    except VerifyTokenExpiresError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verify token has expired"
        )
    return VerifyEmailSuccess(
        user_id=auth_data.id,
        email=auth_data.email
    )

@router.post(
    '/login',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": TokenError},
        401: {"model": TokenError},
        500: {"detail": "Internal server error"}
    },
    summary='Login',
    description='Login using email and password using JWT token and Refresh-Token (for refresh-token you need to add bool remember_me=true)'
)
async def login_user(content: LoginSchema, response: Response, db: AsyncSession = Depends(get_db)) -> Token:
    if content.email == settings.EMAIL:
        if content.password == settings.PASSWORD:
            access_token = await create_access_token(data={"role": "admin"})
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='lax',
                secure=False,
                max_age=2700
            )
            return Token(
                access_token='nah',
                refresh_token='nah',
                token_type='admin'
            )
    auth = await AuthService.get(session=db, email=content.email)
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email or password is incorrect'
        )
    
    if auth.is_verified == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email is not verified"
        )
        
    if await verify_password(content.password, auth.password_hash) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email or password is incorrect'
        )
    access_token = await create_access_token(data={"user_id": str(auth.id)})
    refresh_token = None
    if content.remember_me is True:
        await AuthService.update_rem(session=db, id=auth.id, rem=content.remember_me)
        token_id, refresh_token, expire = await create_refresh_token(remember_me=True)
        ref_token = await RememberService.create(session=db, token=token_id, auth_acc_id=auth.id, expires_at=expire)
    else:
        await AuthService.update_rem(session=db, id=auth.id, rem=content.remember_me)
        token_id, refresh_token, expire = await create_refresh_token(remember_me=False)
        ref_token = await RememberService.create(session=db, token=token_id, auth_acc_id=auth.id, expires_at=expire)
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        samesite='lax',
        secure=False,
        max_age=2700
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post(
    '/refresh',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": TokenError},
        401: {"model": TokenError},
        500: {"detail": "Internal server error"}
    },
    summary="Refresh JWT",
    description='Refresh JWT token using refresh-token. Return JWT Token and new refresh token'
)
async def refresh_jwt(response: Response, refresh_data = Depends(get_current_refresh_data), db: AsyncSession = Depends(get_db)) -> Token:
    auth = await AuthService.get(db, id=refresh_data.auth_account_id)
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User with this token not found'
        )
    access_token = await create_access_token(data={"user_id": str(auth.id)})
    await RememberService.delete(db, refresh_data.id)
    if auth.need_to_be_remembered == True:
        print('yeah')
        token_id, refresh_token, expire = await create_refresh_token(remember_me=True)
    else:
        token_id, refresh_token, expire = await create_refresh_token(remember_me=False)
    ref_token = await RememberService.create(session=db, token=token_id, auth_acc_id=auth.id, expires_at=expire)
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        samesite='lax',
        secure=False,
        max_age=2700
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post(
    '/logout',
    response_model=None,
    status_code=204,
    responses={
        400: {"model": TokenError},
        401: {"model": TokenError},
        500: {"detail": "Internal server error"}
    },
    summary='Logout',
    description='Revoking user refresh token'
)
async def logout(response: Response, refresh_data = Depends(get_current_refresh_data), db: AsyncSession = Depends(get_db)) -> Response:
    auth = await AuthService.get(db, id=refresh_data.auth_account_id)
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User with this token not found'
        )
    await RememberService.revoke(db, auth.id)
    response.delete_cookie("access_token")
    return Response(status_code=status.HTTP_204_NO_CONTENT)