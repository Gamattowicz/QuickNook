import logging

from fastapi import APIRouter, HTTPException

from ecommerceapi.database import category_table, database
from ecommerceapi.models.category import Category, CategoryIn

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/{category_id}", response_model=list[Category])
async def find_category(category_id: int):
    logger.info(f"Finding category with id {category_id}")

    query = category_table.select().where(category_table.c.id == category_id)

    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")

    logger.debug(f"Query: {query}")
    return result


@router.post("/", response_model=Category, status_code=201)
async def create_category(category: CategoryIn):
    logger.info("Creating category")

    data = category.model_dump()
    query = category_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/category", response_model=list[Category])
async def get_all_category():
    logger.info("Getting all categories")
    query = category_table.select()

    logger.debug(query)

    return await database.fetch_all(query)
