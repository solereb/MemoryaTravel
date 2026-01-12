from src.core.config import settings
import aiosmtplib
from email.message import EmailMessage


async def send_email_verification(email: str, verification_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Подтверждение регистрации на сайте MemoryaTravel"
    msg["From"] = settings.SMTP_USER
    msg["TO"] = email
    text = (
        f'Привет! Перейди по ссылке ниже для подтверждения своей регистрации, в ином случае ты не сможешь пользоваться сервисом\n\n\n\n'
        f''
        f''
        f'Ссылка для подтверждения:\n'
        f'{verification_link}'
        f'\n\n\n\n'
        f''
        f''
        f''
        f'Если эту регистрацию соверишили не вы, то проигнорируйте данное сообщение'
        
    )
    msg.set_content(text)
    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.SMTP_USER,
        password=settings.GOOGLE_PASSWORD
    )


async def send_email_reset(email: str, reset_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Смена пароля на MemoryaTravel"
    msg["From"] = settings.SMTP_USER
    msg["TO"] = email
    text = (
        f'Привет! Перейди по ссылке ниже для смены пароля\n\n\n\n'
        f''
        f''
        f'Ссылка для смены:\n'
        f'{reset_link}'
        f'\n\n\n\n'
        f''
        f''
        f''
        f'Если этот запрос соверишили не вы, то проигнорируйте данное сообщение'
        
    )
    msg.set_content(text)
    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.SMTP_USER,
        password=settings.GOOGLE_PASSWORD
    )