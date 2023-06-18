from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from estates.router import router as estate_router
from redis import asyncio as aioredis
from database import create_tables
from appeal.router import router as appeal_router

app = FastAPI(
    title = "3D visualisation"
)

@app.on_event("startup")
async def startup():
    print("Starting up...")
    await create_tables()
    redis = aioredis.from_url("redis://redis:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")



app.include_router(estate_router)
app.include_router(appeal_router)