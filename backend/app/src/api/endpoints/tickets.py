from fastapi import APIRouter, status, Depends, HTTPException, Response, File, UploadFile
from src.api.schemas.tickets import TicketCreate, TicketResponse
from src.api.dependencies import get_current_user, get_db
from src.database.services.ticket_service import TicketService
import uuid
import os
import shutil

router = APIRouter(prefix='/support', tags=['Tickets'])

STORAGE_PATH = os.path.abspath("storage")


@router.post(
    "/tickets",
    response_model=TicketResponse
)
async def create_ticket(data: TicketCreate, cur_user = Depends(get_current_user), db = Depends(get_db)) -> TicketResponse:
    ticket = await TicketService.create(session=db, auth_id=cur_user.id, category=data.category, priority=data.priority, message=data.message)
    return ticket

@router.post(
    "/tickets/{ticket_id}/screenshot"
)
async def upload_image(ticket_id: uuid.UUID, file: UploadFile = File(...), cur_user = Depends(get_current_user), db = Depends(get_db)):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only JPG, PNG, WEBP')
    ticket = await TicketService.get(session=db, ticket_id=ticket_id)
    if ticket.auth_id != cur_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File need to be less then 5 MB')
    print(file.file)
    try:
        uid = str(cur_user.id).zfill(6)
        sub_dir = os.path.join(STORAGE_PATH, "tickets", uid[0:2], uid[2:4])
        os.makedirs(sub_dir, exist_ok=True)
        
        file_path = os.path.join(sub_dir, f'{ticket_id}.webp')
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        return {"detail": "OK"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error during saving image')