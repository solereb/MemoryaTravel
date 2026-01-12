from fastapi import APIRouter, status, Depends, HTTPException, Response

from src.api.dependencies import get_db
from src.database.services.country_service import CountryService
from src.database.services.region_service import RegionService
from src.database.services.errors.coureg_errors import *
from src.api.schemas.geography import CountryResponse, RegionResponse
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import asyncio


router = APIRouter(prefix='/geography', tags=['Geography'])


@router.get(
    '/countries',
    response_model=list[CountryResponse],
    responses={
        200: {"description": "OK"},
        500: {"description": "Internal server error"}
    },
    summary='Return all countries',
    description='Return list with all countries'
)
async def return_countries(db: AsyncSession = Depends(get_db)) -> list[CountryResponse]:
    countries = await CountryService.get_all(session=db)
    return countries

@router.get(
    '/regions/{country_id}',
    response_model=list[RegionResponse],
    responses={
        200: {"description": "OK"},
        400: {"description": "Country with this id not found"},
        500: {"description": "Internal server error"}
    },
    summary='Return all regions',
    description='Return list with all regions in certain country'
)
async def return_regions(country_id: int, db: AsyncSession = Depends(get_db)) -> list[RegionResponse]:
    try:
        regions = await RegionService.get_all_by_country(session=db, country_id=country_id)
    except CouRegError:
        return None
    return regions
