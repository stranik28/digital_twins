from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from database import Base
from datetime import datetime

class WallsMaterial(Base):
    __tablename__ = "walls_materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))

class Real_Estate(Base):
    __tablename__ = "real_estate"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    latitude = Column(String(9))
    longitude = Column(String(9))
    kitchenArea = Column(Float, default=None)
    livingArea = Column(Float, default=None)
    totalArea = Column(Float, default=None)
    floorsTotal = Column(Integer, default=None)
    floorNumber = Column(Integer, default=None)
    price = Column(Integer, default=None)
    wallsMaterial = Column(Integer, ForeignKey("walls_materials.id"), default=None)

class Car_Traffic(Base):
    __tablename__ = "car_traffic"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    latitude = Column(String(9))
    longitude = Column(String(9))
    traffic = Column(Integer, default=None)
    record_date = Column(DateTime, default=datetime.now())

class People_Traffic(Base):
    __tablename__ = "people_traffic"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    latitude = Column(String(9))
    longitude = Column(String(9))
    traffic = Column(Integer, default=None)
    record_date = Column(DateTime, default=datetime.now())

class Water_Level(Base):
    __tablename__ = "water_level"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    latitude = Column(String(9))
    longitude = Column(String(9))
    level = Column(Integer, default=None)
    record_time = Column(DateTime, default=datetime.utcnow)

class Gas_Level(Base):
    __tablename__ = "gas_level"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    latitude = Column(String(9))
    longitude = Column(String(9))
    level = Column(Integer, default=None)
    record_time = Column(DateTime, default=datetime.utcnow)

class Electricity_Level(Base):
    __tablename__ = "electricity_level"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    latitude = Column(String(9))
    longitude = Column(String(9))
    level = Column(Integer, default=None)
    record_time = Column(DateTime, default=datetime.utcnow)

class Trash_Level(Base):
    __tablename__ = "trash_level"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    latitude = Column(String(9))
    longitude = Column(String(9))
    level = Column(Integer, default=None)  
    record_time = Column(DateTime, default=datetime.utcnow)  


# {0: 'None', 1: 'block', 2: 'brick', 3: 'monolith', 4: 'monolithBrick', 5: 'old', 6: 'panel', 7: 'stalin', 8: 'wood'}
