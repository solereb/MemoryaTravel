from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from datetime import datetime

# --- СТАТИСТИКА ---
class AdminStats(BaseModel):
    total_users: int
    total_travels: int
    active_tickets: int

# --- ПОЛЬЗОВАТЕЛИ ---
class UserAdminView(BaseModel):
    id: UUID
    email: EmailStr
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- ТИКЕТЫ (с расширенной информацией) ---
class TicketAdminView(BaseModel):
    id: UUID
    user_email: EmailStr
    auth_id: UUID # Это поле мы склеиваем в эндпоинте
    category: str
    priority: str
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)