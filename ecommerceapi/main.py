from fastapi import FastAPI

from ecommerceapi.routers.category import router as category_router

app = FastAPI()

app.include_router(category_router, prefix="/category")
