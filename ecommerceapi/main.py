from contextlib import asynccontextmanager

from fastapi import FastAPI

from ecommerceapi.database import database
from ecommerceapi.routers.category import router as category_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(category_router, prefix="/category")
