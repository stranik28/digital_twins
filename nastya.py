from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

app = FastAPI()

# Создание подключения к базе данных
engine = create_engine('postgresql://your_user:your_password@your_host/your_database')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Plot(Base):
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    name = Column(String)
    address = Column(String)
    field1 = Column(String)
    field2 = Column(String)
    field3 = Column(String)
    price = Column(Float)

class PlotCreate(BaseModel):
    image: str
    name: str
    address: str
    field1: str
    field2: str
    field3: str
    price: float

@app.get("/plot/{plot_id}")
def get_plot(plot_id: int):
    db = SessionLocal()
    plot = db.query(Plot).filter(Plot.id == plot_id).first()
    db.close()

    if not plot:
        return {"error": "Plot not found"}

    return plot

@app.post("/plot")
def create_plot(plot_data: PlotCreate):
    db = SessionLocal()
    plot = Plot(
        image=plot_data.image,
        name=plot_data.name,
        address=plot_data.address,
        field1=plot_data.field1,
        field2=plot_data.field2,
        field3=plot_data.field3,
        price=plot_data.price
    )
    db.add(plot)
    db.commit()
    db.refresh(plot)
    db.close()
    return plot

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)