from fastapi import APIRouter, status, Depends, HTTPException, Response, UploadFile, File
from fastapi.responses import FileResponse
from src.api.schemas.user import UserUpdateResponse, UserUpdateSchema, ProfileGetResponse
from src.api.dependencies import get_current_user, get_db
from src.database.services.auth_service import AuthAccount
from src.database.services.user_service import UserService
from src.database.services.errors.user_errors import *
from src.database.services.region_service import RegionService
from src.database.services.country_service import CountryService
import io
from PIL import Image
import os


router = APIRouter(prefix='/users', tags=['User interactions'])

STORAGE_PATH = os.path.abspath("storage")

@router.patch(
    '/edit_user',
    response_model=UserUpdateResponse,
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Update profile',
    description='Update profile information with age, gender, username'
)
async def patch_user(data: UserUpdateSchema, cur_user = Depends(get_current_user), db = Depends(get_db)) -> UserUpdateResponse:
    try:
        user = await UserService.upgrade_user(session=db, auth_id=cur_user.id, gender=data.gender, age=data.age, country_id=data.country_id, region_id=data.region_id)
    except BadRegion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Region_id (provided country_id doesnt contain provided region_id)')
    return user

@router.get(
    "/avatar",
    responses={
        401: {'description': "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Get profile avatar',
    description='Get profile avatar'
)
async def get_current_user_avatar(current_user = Depends(get_current_user)):
    user_id_str = str(current_user.id).zfill(6)
    file_path = os.path.join(STORAGE_PATH, 'avatars', user_id_str[:2], user_id_str[2:4], f"{user_id_str}.webp")
    if not os.path.exists(file_path):
        file_path = f'{STORAGE_PATH}/defaults/default.webp'
    return FileResponse(
        file_path,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    )

@router.post(
    "/upload_avatar",
    responses={
        200: {'description': "OK"},
        401: {'description': "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Upload avatar'
)
async def upload_avatar(
    file: UploadFile = File(...),
    cur_user = Depends(get_current_user)
):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only JPG, PNG, WEBP')
    
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File need to be less then 5 MB')
    
    try:
        uid = str(cur_user.id).zfill(6)
        sub_dir = os.path.join(STORAGE_PATH, "avatars", uid[0:2], uid[2:4])
        os.makedirs(sub_dir, exist_ok=True)
        
        file_path = os.path.join(sub_dir, f'{uid}.webp')
        
        
        img = Image.open(io.BytesIO(content))
        
        width, height = img.size
        size = min(width, height)
        left = (width - size) / 2
        top = (height - size) / 2
        img = img.crop((left, top, left + size, top + size))
        
        img.resize((400,400), Image.Resampling.LANCZOS)
        
        img.save(file_path, "WEBP", quality=80)
        
        return {"detail": "OK"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error during saving image')        
    
@router.get(
    '/profile',
    response_model=ProfileGetResponse,
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    },
    summary='Get profile',
    description='Get profile info with regions and country'
)
async def get_profile(cur_user = Depends(get_current_user), db = Depends(get_db)) -> ProfileGetResponse:
    profile = await UserService.get_user(session=db, auth_id=cur_user.id)
    country_id, region_id = None, None
    country_name, region_name = None, None
    if profile.country_id is not None:
        country = await CountryService.get(session=db, country_id=profile.country_id)
        country_id = country.id
        country_name = country.name_ru
        if profile.region_id is not None:
            region = await RegionService.get_by_id(session=db, region_id=profile.region_id)
            region_id = region.id
            region_name = region.name_ru
    return ProfileGetResponse(
        email = cur_user.email,
        username = profile.username,
        age = profile.age,
        gender = profile.gender,
        country_id = country_id,
        country_name = country_name,
        region_id = region_id,
        region_name = region_name
    )