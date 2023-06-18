from fastapi import APIRouter, Depends, HTTPException
from estates.repository import EsateRepository
from estates.schemas import real_EstateBase, EstateResponse, GetEstate
from exceptions import ObjectDoesNotExist
from database import get_async_session
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime

router = APIRouter(prefix="/estates", tags=["estates"])


@router.get("/price", response_model=EstateResponse)
# @cache(expire=86400)
async def get_estate_price(latitude:str, longitude:str, db: AsyncSession = Depends(get_async_session)):
    try:
        return await EsateRepository.get_estate_price(db, latitude, longitude)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.post("/", response_model=real_EstateBase)
async def create_estate(estate: real_EstateBase, db: AsyncSession = Depends(get_async_session)):
    try:
        return await EsateRepository.create_estate(db, estate)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.get("/prediction", response_model=real_EstateBase)
# @cache(expire=86400)
async def get_prediction(id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        return await EsateRepository.get_prediction(db, id)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.get("/estate", response_model=List[GetEstate])
# @cache(expire=86400)
async def get_estate(latitude:str, longitude:str, db: AsyncSession = Depends(get_async_session)):
    try:
        return await EsateRepository.get_estate(db, latitude, longitude)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.get("/area", response_model=List[GetEstate])
# @cache(expire=86400)
async def get_estate(latitude1:str, longitude1:str, latitude2:str, longitude2:str,\
                    filter:str,time:datetime, db: AsyncSession = Depends(get_async_session)):
    try:
        return await EsateRepository.get_area(time, filter, latitude1, longitude1, latitude1,\
                                            latitude2, longitude2, db)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)