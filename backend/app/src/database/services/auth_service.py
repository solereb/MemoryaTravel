from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.database.models.auth_model import AuthAccount
from src.database.services.errors.auth_errors import *
from datetime import datetime
import uuid


class AuthService:
    @staticmethod
    async def create(
        session: AsyncSession,
        email: str, 
        password_hash: str
    ) -> AuthAccount:
        try:
            from datetime import datetime, timedelta
            expires_at = datetime.now() + timedelta(hours=24)
            auth_account = AuthAccount(
                email=email, 
                password_hash=password_hash, 
                verification_token_expires_at=expires_at
            )
            session.add(auth_account)
            await session.commit()
            await session.refresh(auth_account)
            return auth_account
        except IntegrityError as e:
            await session.rollback()
            raise EmailAlreadyExistsError(f"Account with email '{email}' already exists.") from e
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseServiceError(f'Service error: {e}')
        except Exception as e:
            await session.rollback()
            raise DatabaseServiceError(f'Service error: {e}')
    
    @staticmethod
    async def update_reset(
        session: AsyncSession,
        email: str | None = None,
        user_id: uuid.UUID | None = None
    ) -> AuthAccount | None:
        try:
            if email is not None:
                q = await session.execute(select(AuthAccount).where(AuthAccount.email == email))
                auth = q.scalar_one_or_none()
                if auth is None:
                    return None
                auth.reset_token = uuid.uuid4()
                await session.commit()
                await session.refresh(auth)
                return auth
            elif user_id is not None:
                q = await session.execute(select(AuthAccount).where(AuthAccount.id == user_id))
                auth = q.scalar_one_or_none()
                if auth is None:
                    return None
                auth.reset_token = None
                await session.commit()
                await session.refresh(auth)
                return auth
        except Exception as e:
            await session.rollback()
            raise DatabaseServiceError(f'Service error: {e}')
    
    @staticmethod
    async def update_rem(
        session: AsyncSession,
        id: uuid.UUID,
        rem: bool
    ) -> AuthAccount | None:
        try:
            user = await AuthService.get(session=session, id=id)
            user.need_to_be_remembered = rem
            await session.commit()
            await session.refresh(user)
            return user
        except Exception as e:
            await session.rollback()
            raise DatabaseServiceError(f'Service error: {e}')
        
    @staticmethod
    async def get(
        session: AsyncSession,
        email: str | None = None,
        id : uuid.UUID | None = None,
        verification_token: uuid.UUID | None = None,
        reset_token: uuid.UUID | None = None
    ) -> AuthAccount | None:
        try:
            if email:
                q = await session.execute(select(AuthAccount).where(AuthAccount.email == email))
            elif id:
                q = await session.execute(select(AuthAccount).where(AuthAccount.id == id))
            elif verification_token:
                q = await session.execute(select(AuthAccount).where(AuthAccount.verification_token == verification_token))
            elif reset_token:
                q = await session.execute(select(AuthAccount).where(AuthAccount.reset_token == reset_token))
            else:
                return None
            return q.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseServiceError(f'Service error: {e}')
        except Exception as e:
            raise DatabaseServiceError(f'Service error: {e}')
            
    @staticmethod
    async def verify_email(
        session: AsyncSession,
        verification_token: uuid.UUID
    ) -> AuthAccount | None:
        try:
            auth_account = await AuthService.get(session=session, verification_token=verification_token)
            if auth_account == None:
                raise AccountNotFoundError(f'Account with token {verification_token} not found')
        
            if auth_account.is_verified:
                raise IsAlreadyVerified(f'Account with token {verification_token} is already verified')
            
            if auth_account.verification_token_expires_at < datetime.now():
                raise VerifyTokenExpiresError(f'Verify token expired')
            
            auth_account.is_verified = True
            auth_account.verification_token = None
            auth_account.verification_token_expires_at = None
            await session.commit()
            await session.refresh(auth_account)
            return auth_account
        except AccountNotFoundError as e:
            await session.rollback()
            raise e 
        except IsAlreadyVerified as e:
            await session.rollback()
            raise e
        except VerifyTokenExpiresError as e:
            await session.rollback()
            raise e
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseServiceError(f'Service error: {e}')
        except Exception as e:
            await session.rollback()
            raise DatabaseServiceError(f'Service error: {e}')
    
    @staticmethod
    async def update_password(
        session: AsyncSession,
        user_id: uuid.UUID,
        password_hash: str
    ) -> AuthAccount | None:
        try:
            auth = await AuthService.get(session=session, id=user_id)
            if auth is None:
                return None
            auth.password_hash = password_hash
            await session.commit()
            await session.refresh(auth)
            return auth
        except Exception as e:
            await session.rollback()
            raise DatabaseServiceError(f'Service error: {e}')
    
    @staticmethod
    async def get_all(
        session: AsyncSession
    ):
        q = await session.execute(select(AuthAccount))
        auths = q.scalars().all()
        return auths

    @staticmethod
    async def delete(
        session: AsyncSession,
        auth_id: uuid.UUID
    ):
        q = await session.execute(delete(AuthAccount).where(AuthAccount.id == auth_id))
        await session.commit()