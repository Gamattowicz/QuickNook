import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from api.database import category_table, database
from api.models.category import Category, CategoryIn
from api.models.pagination import PaginatedResponse
from api.models.user import User
from api.security import get_current_user
from api.utils.pagination_helpers import paginate

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", response_model=Category, status_code=201)
async def create_category(
    category: CategoryIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Creating category")

    data = category.model_dump()
    query = category_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/category", response_model=PaginatedResponse[Category])
async def get_all_category(
    request: Request,
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0),
):
    path = "category/category"

    return await paginate(
        request, page, per_page, category_table, database, path, Category
    )


async def find_category(category_id: int):
    logger.info(f"Finding category with id {category_id}")

    query = category_table.select().where(category_table.c.id == category_id)

    logger.debug(query)

    return await database.fetch_one(query)
