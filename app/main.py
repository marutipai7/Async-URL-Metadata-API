import logging
from fastapi import FastAPI
from app.api.routes import router
from app.db.database import engine
from app.models.metadata import Base
from contextlib import asynccontextmanager
from app.db.redis import close_redis
from app.core.middleware import timing_middleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )

    yield

    await close_redis()
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.middleware("http")(timing_middleware)
app.include_router(router)

@app.get("/")
def root():
    return {"Message": "ASYNC URL METADATA API PROJECT IS RUNNING"}