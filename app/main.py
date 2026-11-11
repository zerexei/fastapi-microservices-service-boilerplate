from contextlib import asynccontextmanager

from config import settings
from fastapi import FastAPI

from app.core.cache import redis_client
from app.core.database import engine
from app.models import SQLModel
from app.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
  async with engine.begin() as conn:
    await conn.run_sync(SQLModel.metadata.create_all)

  await redis_client.ping()

  yield

  await redis_client.close()
  await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(user_router)


@app.get("/healthz", tags=["Health"])
async def health_check():
  return {"status": "healthy", "service": settings.APP_NAME}