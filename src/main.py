from controllers import DataController,ProjectController,BaseController
from routes.data import data_router
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from helpers.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(
        settings.MONGODB_URL
    )

    app.db_client = app.mongo_conn[
        settings.MONGODB_DATABASE
    ]

    yield

    # Shutdown
    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)

app.include_router(data_router)