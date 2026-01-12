from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import auth, reset, user, geography, travels, tickets, admin
from src.database.core.session import create_tables
from contextlib import asynccontextmanager
import logging

logging.getLogger("uvicorn.access").handlers = logging.getLogger().handlers
logging.getLogger("uvicorn.access").propagate = True
logging.getLogger("uvicorn.error").handlers = logging.getLogger().handlers
logging.getLogger("uvicorn.error").propagate = True
logging.getLogger("fastapi").handlers = logging.getLogger().handlers
logging.getLogger("fastapi").propagate = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    from src.utils.email import send_email_verification
    print("API запущено")
    yield
    print("Приложение выключается")


app = FastAPI(title='My App', version='0.0.1', lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://192.168.0.106:5500", "http://0.0.0.0:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
    max_age=600,
)

app.include_router(auth.router)
app.include_router(reset.router)
app.include_router(user.router)
app.include_router(geography.router)
app.include_router(travels.router)
app.include_router(tickets.router)
app.include_router(admin.router)