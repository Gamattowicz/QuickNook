import logging

from fastapi import APIRouter, HTTPException

from ecommerceapi.database import database, product_table
from ecommerceapi.models.product import Product, ProductIn
from ecommerceapi.routers.category import find_category

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", response_model=Product, status_code=201)
async def create_product(product: ProductIn):
    logger.info("Creating product")

    category = await find_category(product.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    data = product.model_dump()
    query = product_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/product", response_model=list[Product])
async def get_all_product():
    logger.info("Getting all products")

    query = product_table.select()

    logger.debug(query)

    return await database.fetch_all(query)


@router.get("/{product_id}", response_model=Product)
async def find_product(product_id: int):
    logger.info(f"Finding product with id {product_id}")

    query = product_table.select().where(product_table.c.id == product_id)

    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    logger.debug(query)
    return result
