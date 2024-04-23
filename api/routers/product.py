import logging
import os
from pathlib import Path
from typing import Annotated, Optional

import aiofiles
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Request,
    UploadFile,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select

from api.database import category_table, database, product_table
from api.models.filtering import ProductFilter
from api.models.pagination import PaginatedResponse
from api.models.product import Product, ProductWithCategoryName
from api.models.sorting import ProductSortOptions
from api.models.user import User
from api.security import get_current_user
from api.utils.filtering_helpers import apply_filters
from api.utils.pagination_helpers import paginate
from api.utils.product_helpers import (
    create_thumbnail,
    is_file_too_large,
    sanitize_filename,
)
from api.utils.sorting_helpers import apply_sorting

router = APIRouter()

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024 * 1024
MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

THUMBNAIL_SIZE = (128, 128)

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "images"
THUMBNAIL_DIR = BASE_DIR / "thumbnails"


@router.post("/", response_model=Product, status_code=201)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    file: Optional[UploadFile] = File(None),
):
    try:
        logger.info("Creating product")

        data = {
            "name": name,
            "description": description,
            "price": price,
            "category_id": category_id,
            "image": None,
        }

        logger.debug(f"DATA: {data}")

        if file:
            logger.debug(f"File {file}\n {file.content_type}\n {file.filename}")

            if file.content_type not in ALLOWED_IMAGE_TYPES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image type. Available image type are {ALLOWED_IMAGE_TYPES}",
                )

            if await is_file_too_large(file, MAX_IMAGE_SIZE, CHUNK_SIZE):
                raise HTTPException(
                    status_code=400,
                    detail=f"The image is too large. Max size is {MAX_IMAGE_SIZE}",
                )
            file.file.seek(0)

            file_ext = os.path.splitext(file.filename)[1]
            if file_ext.lower() not in ALLOWED_IMAGE_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file extension. Only available file extension are: {ALLOWED_IMAGE_EXTENSIONS}",
                )

            safe_filename = sanitize_filename(file.filename)
            file_location = IMAGE_DIR / safe_filename
            IMAGE_DIR.mkdir(exist_ok=True)

            logger.debug(f"Safe filename: {safe_filename}")
            logger.debug(f"File location: {file_location}")

            async with aiofiles.open(file_location, "wb") as out_file:
                while chunk := await file.read(CHUNK_SIZE):
                    await out_file.write(chunk)

            data["image"] = str(file_location)

            THUMBNAIL_DIR.mkdir(exist_ok=True)

            thumbnail_path = await create_thumbnail(
                file_location, THUMBNAIL_SIZE, THUMBNAIL_DIR
            )
            data["thumbnail"] = str(thumbnail_path)

        query = product_table.insert().values(data)

        logger.debug(query)

        last_record_id = await database.execute(query)
        return {**data, "id": last_record_id}

    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed.")

    except IOError as e:
        logger.error(f"File IO error: {e}")
        raise HTTPException(status_code=500, detail="File handling operation failed.")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/product", response_model=PaginatedResponse[ProductWithCategoryName])
async def get_all_product(
    request: Request,
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0),
    sort: Optional[ProductSortOptions] = Query(None),
    filters: ProductFilter = Depends(),
):
    path = "product/product"
    product_with_category_query = select(
        product_table.c.name,
        product_table.c.description,
        product_table.c.price,
        category_table.c.name.label("category_name"),
        product_table.c.image,
        product_table.c.id,
        product_table.c.thumbnail,
    ).join(category_table, product_table.c.category_id == category_table.c.id)

    filters_dict = {k: v for k, v in filters.dict().items() if v is not None}
    query_with_filters, filters_kv_pairs = apply_filters(
        filters_dict, product_with_category_query
    )

    if sort:
        query_with_filters = apply_sorting(sort, query_with_filters)

    return await paginate(
        request,
        page,
        per_page,
        product_table,
        database,
        path,
        query_with_filters,
        filters_kv_pairs,
        sort.value if sort else None,
    )


@router.get("/{product_id}", response_model=ProductWithCategoryName)
async def find_product(product_id: int):
    logger.info(f"Finding product with id {product_id}")

    query = (
        select(
            [
                product_table.c.name,
                product_table.c.description,
                product_table.c.price,
                category_table.c.name.label("category_name"),
                product_table.c.image,
                product_table.c.id,
                product_table.c.thumbnail,
            ]
        )
        .select_from(
            product_table.join(
                category_table, product_table.c.category_id == category_table.c.id
            )
        )
        .where(product_table.c.id == product_id)
    )

    return await database.fetch_one(query)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info(f"Deleting product with id {product_id}")

    async with database.transaction():
        select_query = product_table.select().where(product_table.c.id == product_id)
        product = await database.fetch_one(select_query)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        delete_query = product_table.delete().where(product_table.c.id == product_id)
        await database.execute(delete_query)

    return {"message": "Product deleted successfully."}
