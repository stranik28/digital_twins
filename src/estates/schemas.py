from pydantic import BaseModel


# to pydantic model

class real_EstateBase(BaseModel):
    name: str
    latitude: str
    longitude: str
    kitchenArea: float = None
    livingArea: float = None
    totalArea: float
    floorsTotal: int = None
    floorNumber: int = None
    price: int
    wallsMaterial: int = None


class EstateCreate(real_EstateBase):
    id: int

class EstateResponse(BaseModel):
    number: int
    price: float

class GetEstate(BaseModel):
    id: int
    name: str
    totalArea: float