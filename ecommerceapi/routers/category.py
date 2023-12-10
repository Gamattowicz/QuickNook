from fastapi import APIRouter

from ecommerceapi.database import category_table, database
from ecommerceapi.models.category import Category, CategoryIn

router = APIRouter()


async def find_category(category_id: int):
    query = category_table.select().where(category_table.c.id == category_id)
    return await database.fetch_one(query)


@router.post("/", response_model=Category, status_code=201)
async def create_category(category: CategoryIn):
    data = category.model_dump()
    query = category_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}
    # last_record_id = len(category_table)
    # new_category = {**data, "id": last_record_id}
    # category_table[last_record_id] = new_category
    # return new_category


@router.get("/category", response_model=list[Category])
async def get_all_category():
    query = category_table.select()
    return await database.fetch_all(query)
