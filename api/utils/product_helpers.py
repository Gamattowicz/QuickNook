import datetime
import re
from io import BytesIO
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from PIL import Image


def sanitize_filename(filename: str) -> str:
    filename = Path(filename).name
    filename = re.sub(r"[^\w\s.-]", "", filename)
    filename = filename[:255]

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{timestamp}_{filename}"


async def is_file_too_large(file: UploadFile, max_size: int, chunk_size: int) -> bool:
    total_size = 0
    while chunk := await file.read(chunk_size):
        total_size += len(chunk)
        if total_size > max_size:
            return True
    return False


async def create_thumbnail(
    image_path: Path, thumbnail_size: int, thumbnail_dir: Path
) -> Path:
    with Image.open(image_path) as img:
        img.thumbnail(thumbnail_size)
        thumbnail_path = thumbnail_dir / f"thumbnail_{image_path.stem}.png"

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        async with aiofiles.open(thumbnail_path, "wb") as out_file:
            await out_file.write(img_bytes)

        return thumbnail_path
