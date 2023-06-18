from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from estates.router import router as estate_router
from forecast.router import router as forecast_router
from redis import asyncio as aioredis
from database import create_tables
from appeal.router import router as appeal_router
import asyncio
from fastapi import WebSocket

app = FastAPI(
    title = "3D visualisation"
)

@app.on_event("startup")
async def startup():
    print("Starting up...")
    await create_tables()
    redis = aioredis.from_url("redis://redis:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

connected_clients = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True:
            # Generate mock data
            mock_data = {
                "lat": 12.345,
                "long": 67.890,
                "estates": [
                    {"id": 1, "lat": 12.345, "long": 67.890, "price": 100000},
                    {"id": 2, "lat": 23.456, "long": 45.678, "price": 150000},
                    # Add more estate objects here
                ]
            }

            # Send the mock data as JSON to all connected clients
            for client in connected_clients:
                await client.send_json(mock_data)

            # Wait for a while before sending the next set of mock data
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        await websocket.close()

app.include_router(estate_router)
app.include_router(appeal_router)
app.include_router(forecast_router)