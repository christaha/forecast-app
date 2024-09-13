import asyncio
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.routers.temperature import router
from app.services.forecast_tracker import ForecastTracker

# As an improvement could configure from environment variable
logging.getLogger().setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Start schedule to get forecast data
    tracker = ForecastTracker()
    asyncio.create_task(tracker.start())
    yield


app = FastAPI(
    title="Amazing Forecast API",
    version=settings.version,
    docs_url="/api/docs",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api")
