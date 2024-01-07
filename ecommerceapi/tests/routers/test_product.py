import contextlib
import pathlib
from io import BytesIO
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from ecommerceapi.routers import product


async def create_product_with_image(
    name: str,
    description: str,
    price: float,
    category_id: int,
    image_content: bytes,
    image_content_type: str,
    image_filename: str,
    async_client: AsyncClient,
) -> dict:
    form_data = {
        "name": (None, name),
        "description": (None, description),
        "price": (None, str(price)),
        "category_id": (None, str(category_id)),
        "file": (image_filename, image_content, image_content_type),
    }
    response = await async_client.post("/product/", data=form_data)
    return response.json()


@pytest.fixture()
async def created_product_with_image(async_client: AsyncClient, created_category: dict):
    image_content = BytesIO(open("test_image.jpg", "rb").read())

    return await create_product_with_image(
        "Test Product",
        "Test Description",
        4.00,
        image_content,
        "image/jpeg",
        "test_image.jpg",
        created_category["id"],
        async_client,
    )


@pytest.fixture()
def sample_image(fs) -> pathlib.Path:
    path = (
        pathlib.Path(__file__).parent.parent.parent / "images" / "test_image.png"
    ).resolve()
    fs.create_file(path)
    return path


@pytest.fixture(autouse=True)
def aiofiles_mock_open(mocker):
    mock_open = mocker.patch("aiofiles.open")

    @contextlib.asynccontextmanager
    async def async_file_open(fname: str, mode: str = "r"):
        out_fs_mock = mocker.AsyncMock(name=f"async_file_open:{fname!r}/{mode!r}")
        with open(fname, mode) as f:
            out_fs_mock.read.side_effect = f.read
            out_fs_mock.write.side_effect = f.write
            yield out_fs_mock

    mock_open.side_effect = async_file_open
    return mock_open


@pytest.fixture
def mock_create_thumbnail(mocker):
    mock = AsyncMock(return_value=product.THUMBNAIL_DIR / "thumbnail_test_image.png")
    mocker.patch.object(product, "create_thumbnail", new=mock)
    return mock


@pytest.mark.anyio
async def test_create_product_with_image(
    async_client: AsyncClient,
    created_category: dict,
    sample_image: pathlib.Path,
    mock_create_thumbnail: AsyncMock,
):
    name = "Test Product"
    description = "Test Description"
    price = 4.00
    category_id = created_category["id"]

    form_data = {
        "name": (None, name),
        "description": (None, description),
        "price": (None, str(price)),
        "category_id": (None, str(category_id)),
    }
    response = await async_client.post(
        "/product/", data=form_data, files={"file": open(sample_image, "rb")}
    )
    print(response.json())
    assert response.status_code == 201
    assert {
        "id": 1,
        "name": name,
        "description": description,
        "price": price,
        "category_id": category_id,
    }.items() <= response.json().items()
    assert "test_image.png" in response.json()["image"]
    assert "thumbnail_test_image.png" in response.json()["thumbnail"]


@pytest.mark.anyio
async def test_create_product(async_client: AsyncClient, created_category: dict):
    name = "Test Product"
    description = "Test Description"
    price = 4.00
    category_id = created_category["id"]
    form_data = {
        "name": (None, name),
        "description": (None, description),
        "price": (None, str(price)),
        "category_id": (None, str(category_id)),
    }
    response = await async_client.post("/product/", data=form_data)

    assert response.status_code == 201
    assert {
        "id": 1,
        "name": name,
        "description": description,
        "price": price,
        "category_id": category_id,
        "image": None,
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_product_missing_data(async_client: AsyncClient):
    response = await async_client.post("/product/", json={})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_products(async_client: AsyncClient, created_product: dict):
    response = await async_client.get("/product/product")

    assert response.status_code == 200
    assert response.json() == [created_product]
