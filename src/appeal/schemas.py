from pydantic import BaseModel
from datetime import datetime
import uuid

class Appeal(BaseModel):
    name: str
    email: str
    address: str
    message: str

class CreateAppeal(Appeal):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: int