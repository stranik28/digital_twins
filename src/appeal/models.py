from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
import datetime

class Appeal(Base):
    __tablename__ = "appeals"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(64))
    email = Column(String(64))
    message = Column(String(64))
    address = Column(String(64))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Integer, default=0)

class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))