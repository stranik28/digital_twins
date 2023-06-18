from appeal.schemas import Appeal,CreateAppeal
from appeal.models import Appeal
from exceptions import ObjectDoesNotExist
from sqlalchemy import insert, select
import uuid
from typing import List
from datetime import datetime

class AppealRepository():

    async def create_appeal(db, appeal: Appeal) -> CreateAppeal:
        query = insert(Appeal).values(**appeal.__dict__)
        await db.execute(query)
        await db.commit()
        query = select(Appeal).where(Appeal.email == appeal.email)
        query = await db.execute(query)
        query = query.scalars().first()
        if query is None:
            raise ObjectDoesNotExist("Appeal not found")
        return CreateAppeal(**query.__dict__)
    
    async def get_appeal(db, id: str) -> CreateAppeal:
        query = select(Appeal).where(Appeal.id == id)
        query = await db.execute(query)
        query = query.scalars().first()
        if query is None:
            raise ObjectDoesNotExist("Appeal not found")
        return CreateAppeal(**query.__dict__)
    
    async def get_appeals(db, email: str) -> List[CreateAppeal]:
        query = select(Appeal).where(Appeal.email == email)
        query = await db.execute(query)
        query = query.scalars().all()
        print(query)
        if query is None:
            raise ObjectDoesNotExist("Appeal not found")
        return [CreateAppeal(**i.__dict__) for i in query]
    
    async def get_all_appeals(db) -> List[CreateAppeal]:
        query = select(Appeal)
        query = await db.execute(query)
        query = query.scalars().all()
        if query is None:
            raise ObjectDoesNotExist("Appeal not found")
        return [CreateAppeal(**i.__dict__) for i in query]
    
    async def update_appeal_status(db, id: uuid, status: str) -> CreateAppeal:
        query = select(Appeal).where(Appeal.id == id)
        query = await db.execute(query)
        query = query.scalars().first()
        if query is None:
            raise ObjectDoesNotExist("Appeal not found")
        query.status = status
        query.updated_at = datetime.now()
        await db.commit()
        return CreateAppeal(**query.__dict__)