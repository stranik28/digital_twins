from fastapi import APIRouter, Depends, HTTPException
from appeal.repository import AppealRepository
from appeal.schemas import Appeal, CreateAppeal
from exceptions import ObjectDoesNotExist
from database import get_async_session
from typing import List

router = APIRouter(prefix="/appeal", tags=["appeal"])

@router.post("/", response_model=CreateAppeal)
async def create_appeal(appeal: Appeal, db = Depends(get_async_session)):
    try:
        return await AppealRepository.create_appeal(db, appeal)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.get("/", response_model=CreateAppeal)
async def get_appeal(id: str, db = Depends(get_async_session)):
    try:
        return await AppealRepository.get_appeal(db, id)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.get("/all/{email}", response_model=List[CreateAppeal])
async def get_appeals(email: str, db = Depends(get_async_session)):
    try:
        return await AppealRepository.get_appeals(db, email)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.get("/all", response_model=List[CreateAppeal])
async def get_all_appeals(db = Depends(get_async_session)):
    try:
        return await AppealRepository.get_all_appeals(db)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.put("/{id}", response_model=CreateAppeal)
async def update_appeal_status(id: str, status:int, db = Depends(get_async_session)):
    try:
        return await AppealRepository.update_appeal_status(db, id, status)
    except ObjectDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)