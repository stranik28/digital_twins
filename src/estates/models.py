from sqlalchemy import Column, Integer, String, ForeignKey, Float
from database import Base

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



# {0: 'None', 1: 'block', 2: 'brick', 3: 'monolith', 4: 'monolithBrick', 5: 'old', 6: 'panel', 7: 'stalin', 8: 'wood'}
