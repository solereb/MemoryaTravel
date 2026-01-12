from fastapi import APIRouter, status, Depends, HTTPException, Response, File, UploadFile
from fastapi.responses import FileResponse
from src.api.schemas.admin import AdminStats, UserAdminView, TicketAdminView
from src.api.dependencies import get_current_user, get_db, get_is_admin
from src.database.services.user_service import UserService
from src.database.services.auth_service import AuthService
from src.database.services.ticket_service import TicketService
from src.database.services.travel_service import TravelService
from typing import List
import uuid
import os
import shutil

router = APIRouter(prefix='/admin', tags=['Admin'])

STORAGE_PATH = os.path.abspath("storage")


@router.get(
    "/users",
    response_model=List[UserAdminView]
)
async def create_ticket(cur_user = Depends(get_is_admin), db = Depends(get_db)):
    if cur_user == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    auths = await AuthService.get_all(session=db)
    return auths

@router.get(
    "/tickets",
    response_model=List[TicketAdminView]
)
async def get_tickets(cur_user = Depends(get_is_admin), db = Depends(get_db)):
    if cur_user == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    tickets = await TicketService.get_all(session=db)
    for i in tickets:
        auth = await AuthService.get(session=db, id=i.auth_id)
        i.user_email = auth.email
    return tickets

@router.get(
    "/support/{ticket_id}/{user_id}/screenshot"
)
async def get_screenshot(ticket_id: uuid.UUID, user_id: uuid.UUID, cur_user = Depends(get_is_admin), db = Depends(get_db)):
    if cur_user == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    user_id_str = str(user_id).zfill(6)
    file_path = os.path.join(STORAGE_PATH, 'tickets', user_id_str[:2], user_id_str[2:4], f"{ticket_id}.webp")
    if not os.path.exists(file_path):
        file_path = f'{STORAGE_PATH}/defaults/default_travel.webp'
    return FileResponse(
        file_path,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    )

@router.get(
    "/stat"
)
async def get_stat(cur_user = Depends(get_is_admin), db = Depends(get_db)):
    if cur_user == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    auths = await AuthService.get_all(session=db)
    tickets = await TicketService.get_all(session=db)
    travels = await TravelService.get_all(session=db)
    return AdminStats(
        total_users = len(auths),
        active_tickets = len(tickets),
        total_travels = len(travels)
    )

@router.post(
    "/users/{user_id}/verify"
)
async def verify_user(user_id: uuid.UUID, cur_user = Depends(get_is_admin), db = Depends(get_db)):
    if cur_user == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    auth = await AuthService.get(session=db, id=user_id)
    await AuthService.verify_email(session=db, verification_token=auth.verification_token)
    return {'OK'}

@router.delete(
    "/users/{user_id}"
)
async def verify_user(user_id: uuid.UUID, cur_user = Depends(get_is_admin), db = Depends(get_db)):
    if cur_user == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await AuthService.delete(session=db, auth_id=user_id)
    return {'OK'}

@router.delete(
    "/ticket/{ticket_id}"
)
async def delete_ticket(ticket_id: uuid.UUID, cur_user = Depends(get_is_admin), db = Depends(get_db)):
    if cur_user == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await TicketService.delete(session=db, ticket_id=ticket_id)