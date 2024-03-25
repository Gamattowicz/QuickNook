import logging
import os
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.database import database
from api.logging_conf import configure_logging
from api.routers.category import router as category_router
from api.routers.order import router as order_router
from api.routers.product import router as product_router
from api.routers.user import router as user_router

logger = logging.getLogger(__name__)

origins = [
    "http://localhost:3000",  # React app
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(
    lifespan=lifespan, swagger_ui_parameters={"syntaxHighlight.theme": "tomorrow-night"}
)

app.add_middleware(CorrelationIdMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
images_path = os.path.join(os.path.dirname(__file__), 'images')
thumbnails_path = os.path.join(os.path.dirname(__file__), 'thumbnails')

app.mount("/images", StaticFiles(directory=images_path), name="images")
app.mount("/thumbnails", StaticFiles(directory=thumbnails_path), name="thumbnails")

app.include_router(category_router, prefix="/category")
app.include_router(product_router, prefix="/product")
app.include_router(order_router, prefix="/order")
app.include_router(user_router, prefix="/user")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
