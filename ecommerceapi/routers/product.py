import datetime
import logging
import os
import re
from io import BytesIO
from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image
from sqlalchemy.exc import SQLAlchemyError

from ecommerceapi.database import database, product_table
from ecommerceapi.models.product import Product

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


def sanitize_filename(filename: str) -> str:
    filename = Path(filename).name
    filename = re.sub(r"[^\w\s.-]", "", filename)
    filename = filename[:255]

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{timestamp}_{filename}"


async def is_file_too_large(file: UploadFile, max_size: int) -> bool:
    total_size = 0
    while chunk := await file.read(CHUNK_SIZE):
        total_size += len(chunk)
        if total_size > max_size:
            return True
    return False


async def create_thumbnail(image_path: Path) -> Path:
    with Image.open(image_path) as img:
        img.thumbnail(THUMBNAIL_SIZE)
        thumbnail_path = THUMBNAIL_DIR / f"thumbnail_{image_path.stem}.png"

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        async with aiofiles.open(thumbnail_path, "wb") as out_file:
            await out_file.write(img_bytes)

        return thumbnail_path


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

            if await is_file_too_large(file, MAX_IMAGE_SIZE):
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

            thumbnail_path = await create_thumbnail(file_location)
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
