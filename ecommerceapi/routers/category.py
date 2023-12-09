from fastapi import APIRouter

from ecommerceapi.models.category import Category, CategoryIn

router = APIRouter()
category_table = {}


@router.post("/", response_model=Category, status_code=201)
async def create_category(category: CategoryIn):
    data = category.model_dump()
    last_record_id = len(category_table)
    new_category = {**data, "id": last_record_id}
    category_table[last_record_id] = new_category
    return new_category


@router.get("/category", response_model=list[Category])
async def get_all_category():
    return list(category_table.values())
