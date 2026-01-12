from fastapi import APIRouter, status, Depends, HTTPException, Response, File, UploadFile
from fastapi.responses import FileResponse
from src.api.schemas.travel_schema import TravelResponse, TravelCreateSchema
from src.database.services.travel_service import TravelService
from src.database.services.errors.travel_errors import *
from src.database.services.country_service import CountryService
from src.database.services.region_service import RegionService
from src.api.dependencies import get_current_user, get_db
from typing import List
import shutil
import uuid
import os


router = APIRouter(prefix='/travels', tags=['Travel interactions'])
STORAGE_PATH = os.path.abspath("storage")

@router.post("/{travel_id}/upload-media")
async def upload_travel_media(
    travel_id: uuid.UUID,
    files: List[UploadFile] = File(...),
    cur_user = Depends(get_current_user),
    db = Depends(get_db)
):
    
    travel = await TravelService.get_by_id(session=db, travel_id=travel_id)
    if travel.auth_id != cur_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Dont try upload photos for not your travel')
    uid = str(travel.id).zfill(6)
    sub_dir = os.path.join(
        STORAGE_PATH,
        'travels',
        uid[0:2], 
        uid[2:4], 
        f"travel_{travel_id}"
    )
    os.makedirs(sub_dir, exist_ok=True)

    saved_files = []
    for index, file in enumerate(files):
        if index > 4:
            break
        allowed_types = ["image/jpeg", "image/png", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only JPG, PNG, WEBP')
        filename = f"main.webp" if index == 0 else f"file_{index}.webp"
        file_path = os.path.join(sub_dir, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        saved_files.append(filename)

    return {"status": "OK"}
    
@router.post(
    "/create",
    response_model=TravelResponse,
    responses={
        401: {'description': "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Create Travel',
)
async def create_travel(data: TravelCreateSchema, cur_user=Depends(get_current_user), db = Depends(get_db)) -> TravelResponse:
    new_travel = await TravelService.create_travel(session=db, auth_id=cur_user.id, title=data.title, date=data.date, country_id=data.country_id, region_id=data.region_id, icon_ids=data.icon_ids, description=data.description)
    return new_travel

@router.get(
    "/by_id/{travel_id}",
    response_model=TravelResponse,
    responses={
        400: {'description': 'Travel with this id not found'},
        401: {'description': "Unauthorized"},
        403: {'description': "Not your travel"},
        500: {"description": "Internal server error"}
    },
    summary='Get travel by id'
)
async def get_by_id(travel_id = uuid.UUID, cur_user = Depends(get_current_user), db = Depends(get_db)) -> TravelResponse:
    travel = await TravelService.get_by_id(session=db, travel_id=travel_id)
    
    if travel == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Travel with this id not found')
    elif travel.auth_id != cur_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')
    else:
        country = await CountryService.get(session=db, country_id=travel.country_id)
        region = await RegionService.get_by_id(session=db, region_id=travel.region_id)
        uid = travel_id
        file_path = os.path.join(
            STORAGE_PATH,
            'travels',
            uid[0:2], 
            uid[2:4], 
            f"travel_{travel_id}"
        )
        media = []
        if os.path.exists(file_path):
            possible_files = ['main.webp', 'file_1.webp', 'file_2.webp', 'file_3.webp', 'file_4.webp']
            for name in possible_files:
                new_path = os.path.join(file_path, name)
                print(new_path)
                if os.path.exists(new_path):
                    media.append(name)
        if media == []:
            media.append('default.webp')
        return TravelResponse(
            id=travel.id,
            title=travel.title,
            travel_date=travel.travel_date,
            country_id=travel.country_id,
            region_id=travel.region_id,
            description=travel.description,
            icon_ids=travel.icon_ids,
            country_name=country.name_ru,
            region_name=region.name_ru,
            media = media
        )

@router.delete(
    '/by_id/{travel_id}',
)
async def delete_travel(travel_id: uuid.UUID, cur_user = Depends(get_current_user), db = Depends(get_db)):
    travel = await TravelService.get_by_id(session=db, travel_id=travel_id)
    if travel.auth_id != cur_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')
    await TravelService.delete(session=db, travel_id=travel_id)
    return Response(status_code=status.HTTP_200_OK)

@router.get(
    "/main_image/{travel_id}",
    responses={
        401: {'description': "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Get image of travel'
)
async def get_current_user_avatar(travel_id: uuid.UUID, current_user = Depends(get_current_user), db=Depends(get_db)):
    travel = await TravelService.get_by_id(session=db, travel_id=travel_id)
    if travel.auth_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Dont try get photos for not your travel')
    user_id_str = str(travel_id).zfill(6)
    file_path = os.path.join(STORAGE_PATH, 'travels', user_id_str[:2], user_id_str[2:4], f'travel_{travel_id}', f"main.webp")
    print(file_path)
    if not os.path.exists(file_path):
        file_path = f'{STORAGE_PATH}/defaults/default_travel.png'
    return FileResponse(
        file_path,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            'Pragma': 'no-cache',
            'Expires': '02'
        }
    )

@router.get(
    "/image/{travel_id}/{name}",
    responses={
        401: {'description': "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Get image of travel'
)
async def get_current_user_avatar(travel_id: uuid.UUID, name: str, current_user = Depends(get_current_user), db=Depends(get_db)):
    travel = await TravelService.get_by_id(session=db, travel_id=travel_id)
    if travel.auth_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Dont try get photos for not your travel')
    user_id_str = str(travel_id).zfill(6)
    file_path = os.path.join(STORAGE_PATH, 'travels', user_id_str[:2], user_id_str[2:4], f'travel_{travel_id}', name)
    print(file_path)
    if not os.path.exists(file_path):
        file_path = f'{STORAGE_PATH}/defaults/default_travel.png'
    return FileResponse(
        file_path,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            'Pragma': 'no-cache',
            'Expires': '02'
        }
    )
    
@router.get(
    '/by_country/{country_id}',
    response_model=List[TravelResponse]
)
async def get_by_country(country_id: int, cur_user = Depends(get_current_user), db = Depends(get_db)):
    travels = await TravelService.get_by_country(session=db, auth_id=cur_user.id, country_id=country_id)
    return travels

@router.get(
    '/by_region/{region_id}',
    response_model=List[TravelResponse]
)
async def get_by_country(region_id: int, cur_user = Depends(get_current_user), db = Depends(get_db)):
    travels = await TravelService.get_by_region(session=db, auth_id=cur_user.id, region_id=region_id)
    return travels

@router.get(
    '/my',
    response_model=List[TravelResponse]
)
async def get_travels(cur_user = Depends(get_current_user), db = Depends(get_db)):
    travels = await TravelService.get_by_id(session=db, auth_id=cur_user.id)
    for i in travels:
        country = await CountryService.get(session=db, country_id=i.country_id)
        i.country_name = country.name_ru
        region = await RegionService.get_by_id(session=db, region_id=i.region_id)
        i.region_name = region.name_ru
    return travels