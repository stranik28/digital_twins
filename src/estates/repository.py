from estates.schemas import EstateResponse, GetEstate, real_EstateBase,\
    GetAnalyticsTraffic
from estates.models import Real_Estate, Car_Traffic, People_Traffic, Water_Level,\
    Gas_Level, Electricity_Level, Trash_Level 
from exceptions import ObjectDoesNotExist
from sqlalchemy import insert, select
from typing import List
from estates.predict import predict
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

class EsateRepository:
    
    async def get_estate_price(db, latitude, longitude) -> EstateResponse:
        query = select(Real_Estate)\
                       .where(Real_Estate.latitude == latitude, Real_Estate.longitude == longitude)
        query = await db.execute(query)
        query = query.scalars().all()
        if query is None:
            raise ObjectDoesNotExist("Estate not found")
        if len(query) == 0:
            raise ObjectDoesNotExist("Estate not found")
        price = 0
        area = 0
        for i in query:
            price += i.price
            area = i.totalArea
        if area == 0:
            area = 1
        resp = EstateResponse(number=len(query), price=price/area)
        return resp
    
    async def create_estate(db, estate: real_EstateBase) -> real_EstateBase:
        query = insert(Real_Estate).values(**estate.__dict__)
        await db.execute(query)
        await db.commit()
        return estate
    
    async def get_prediction(db, id: int):
        query = select(Real_Estate)\
                       .where(Real_Estate.id == id)
        query = await db.execute(query)
        query = query.scalars().first()
        estate = real_EstateBase(**query.__dict__)
        price = predict(estate)
        estate.price = price
        return real_EstateBase(**estate.__dict__)

    async def get_estate(db, latitude, longitude) -> List[GetEstate]:
        query = select(Real_Estate)\
                       .where(Real_Estate.latitude == latitude, Real_Estate.longitude == longitude)
        query = await db.execute(query)
        query = query.scalars().all()
        resp = [GetEstate(**i.__dict__) for i in query]
        if query is None:
            raise ObjectDoesNotExist("Estate not found")
        if len(query) == 0:
            raise ObjectDoesNotExist("Estate not found")
        return resp
    
    async def get_area(time:datetime,filter:str, latitude1:str, longitude1:str, latitude2:str, longitude2:str,db: AsyncSession):
        if filter == "Voda":
            query = select(Water_Level)\
                .where(Water_Level.latitude >= latitude1,\
                Water_Level.latitude <= latitude2,\
                Water_Level.longitude >= longitude1,\
                Water_Level.longitude <= longitude2)\
                .order_by(Water_Level.time.desc())
            query = await db.execute(query)
            query = query.scalars().first()
            if query is None:
                raise ObjectDoesNotExist("Записи не найдены")
            resp = GetAnalyticsTraffic(**query.__dict__)
        elif filter == "Trash":
            query = select(Trash_Level)\
                .where(Trash_Level.latitude >= latitude1,\
                Trash_Level.latitude <= latitude2,\
                Trash_Level.longitude >= longitude1,\
                Trash_Level.longitude <= longitude2)\
                .order_by(Trash_Level.time.desc())
            query = await db.execute(query)
            query = query.scalars().first()
            if query is None:
                raise ObjectDoesNotExist("Записи не найдены")
            resp = GetAnalyticsTraffic(**query.__dict__)
        elif filter == "Price":
            query = select(EsateRepository)\
                .where(EsateRepository.latitude >= latitude1,\
                EsateRepository.latitude <= latitude2,\
                EsateRepository.longitude >= longitude1,\
                EsateRepository.longitude <= longitude2)
            query = await db.execute(query)
            query = query.scalars().all()
            resp = [GetEstate(**i.__dict__) for i in query]
        elif filter == "Visiting":
            query = select(People_Traffic)\
                .where(People_Traffic.latitude >= latitude1,\
                People_Traffic.latitude <= latitude2,\
                People_Traffic.longitude >= longitude1,\
                People_Traffic.longitude <= longitude2)\
                .order_by(People_Traffic.time.desc())
            query = await db.execute(query)
            query = query.scalars().first()
            if query is None:
                raise ObjectDoesNotExist("Записи не найдены")
            resp = GetAnalyticsTraffic(**query.__dict__)
        elif filter == "Gas":
            query = select(Gas_Level)\
                .where(Gas_Level.latitude >= latitude1,\
                Gas_Level.latitude <= latitude2,\
                Gas_Level.longitude >= longitude1,\
                Gas_Level.longitude <= longitude2)\
                .order_by(Gas_Level.time.desc())
            query = await db.execute(query)
            query = query.scalars().first()
            if query is None:
                raise ObjectDoesNotExist("Записи не найдены")
            resp = GetAnalyticsTraffic(**query.__dict__)
        elif filter == "Electricity":
            query = select(Electricity_Level)\
                .where(Electricity_Level.latitude >= latitude1,\
                Electricity_Level.latitude <= latitude2,\
                Electricity_Level.longitude >= longitude1,\
                Electricity_Level.longitude <= longitude2)\
                .order_by(Electricity_Level.time.desc())
            query = await db.execute(query)
            query = query.scalars().first()
            if query is None:
                raise ObjectDoesNotExist("Записи не найдены")
            resp = GetAnalyticsTraffic(**query.__dict__)
        elif filter == "Car":
            query = select(Car_Traffic)\
                .where(Car_Traffic.latitude >= latitude1,\
                Car_Traffic.latitude <= latitude2,\
                Car_Traffic.longitude >= longitude1,\
                Car_Traffic.longitude <= longitude2)\
                .order_by(Car_Traffic.time.desc())
            query = await db.execute(query)
            query = query.scalars().first()
            if query is None:
                raise ObjectDoesNotExist("Записи не найдены")
            resp = GetAnalyticsTraffic(**query.__dict__)
        return resp