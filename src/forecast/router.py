from fastapi import APIRouter, Depends, HTTPException
from forecast.forcast import ForcastRepoitory

router = APIRouter(prefix="/forecast", tags=["forecast"])

@router.get("/")
async def get_forecast():
    return ForcastRepoitory.get_forcats_cars()
