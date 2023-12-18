import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from ecommerceapi.database import database
from ecommerceapi.logging_conf import configure_logging
from ecommerceapi.routers.category import router as category_router
from ecommerceapi.routers.order import router as order_router
from ecommerceapi.routers.product import router as product_router
from ecommerceapi.routers.user import router as user_router

logger = logging.getLogger(__name__)


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

app.include_router(category_router, prefix="/category")
app.include_router(product_router, prefix="/product")
app.include_router(order_router, prefix="/order")
app.include_router(user_router, prefix="/user")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
