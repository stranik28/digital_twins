from estates.schemas import EstateResponse, GetEstate
from estates.models import Real_Estate
from exceptions import ObjectDoesNotExist
from sqlalchemy import insert, select
from estates.schemas import real_EstateBase
from typing import List
from estates.predict import predict

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
    
    async def get_area(filter:str, latitude1:str, longitude1:str, latitude2:str, longitude2:str,\
                    db):
        pass