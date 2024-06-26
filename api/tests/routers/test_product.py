import contextlib
import pathlib
from io import BytesIO
from unittest.mock import AsyncMock
from urllib.parse import urljoin

import pytest
from httpx import AsyncClient

from api import security
from api.routers import product
from api.utils import product_helpers


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
    mocker.patch.object(product_helpers, "create_thumbnail", new=mock)
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
async def test_delete_existing_product(
    async_client: AsyncClient, created_product: dict, logged_in_token: str
):
    response = await async_client.delete(
        f"/product/{created_product['id']}",
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_non_existing_product(
    async_client: AsyncClient, logged_in_token: str
):
    non_existing_product_id = 31
    response = await async_client.delete(
        f"/product/{non_existing_product_id}",
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_product_missing_token(
    async_client: AsyncClient, created_product: dict
):
    response = await async_client.delete(f"/product/{created_product['id']}")

    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


@pytest.mark.anyio
async def test_delete_product_expired_token(
    async_client: AsyncClient, created_product: dict, confirmed_user: dict, mocker
):
    mocker.patch("api.security.access_token_expire_minutes", return_value=-1)
    token = security.create_access_token(
        confirmed_user["email"], confirmed_user["role"]
    )
    response = await async_client.delete(
        f"/product/{created_product['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_product_missing_data(async_client: AsyncClient):
    response = await async_client.post("/product/", json={})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_products(
    async_client: AsyncClient, created_product: dict, created_category: dict
):
    response = await async_client.get("/product/product")

    created_product["category_name"] = created_category["name"]
    del created_product["category_id"]
    assert response.status_code == 200
    assert response.json()["results"] == [created_product]


@pytest.mark.anyio
async def test_get_all_products_with_pagination_first_page(
    async_client: AsyncClient,
    created_multiple_product: list,
    created_multiple_category: list,
):
    page = 1
    per_page = 2
    total_product = 6
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}"
    )

    fetched_products = created_multiple_product[(page - 1) * per_page : page * per_page]

    for i in range(len(fetched_products)):
        fetched_products[i]["category_name"] = created_multiple_category[i]["name"]
        del fetched_products[i]["category_id"]

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_product
    assert response.json()["prevPageUrl"] is None
    assert response.json()["results"] == fetched_products

    # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["nextPageUrl"]
        == f"{base_url}product/product?page={page + 1}&per_page={per_page}"
    )


@pytest.mark.anyio
async def test_get_all_products_with_pagination_second_page(
    async_client: AsyncClient,
    created_multiple_product: list,
    created_multiple_category: list,
):
    page = 2
    per_page = 2
    total_product = 6
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}"
    )

    start_index = (page - 1) * per_page
    fetched_products = created_multiple_product[start_index : page * per_page]
    for i in range(len(fetched_products)):
        fetched_products[i]["category_name"] = created_multiple_category[
            start_index + i
        ]["name"]
        del fetched_products[i]["category_id"]

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_product
    assert response.json()["results"] == fetched_products

    # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["prevPageUrl"]
        == f"{base_url}product/product?page={page - 1}&per_page={per_page}"
    )
    assert (
        response.json()["nextPageUrl"]
        == f"{base_url}product/product?page={page + 1}&per_page={per_page}"
    )


@pytest.mark.anyio
async def test_get_all_products_with_pagination_last_page(
    async_client: AsyncClient,
    created_multiple_product: list,
    created_multiple_category: list,
):
    page = 3
    per_page = 2
    total_product = 6
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}"
    )

    start_index = (page - 1) * per_page
    fetched_products = created_multiple_product[start_index : page * per_page]
    for i in range(len(fetched_products)):
        fetched_products[i]["category_name"] = created_multiple_category[
            start_index + i
        ]["name"]
        del fetched_products[i]["category_id"]

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_product
    assert response.json()["nextPageUrl"] is None
    assert response.json()["results"] == fetched_products

    # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["prevPageUrl"]
        == f"{base_url}product/product?page={page - 1}&per_page={per_page}"
    )


@pytest.mark.anyio
async def test_filter_name_products(
    async_client: AsyncClient,
    created_multiple_product: list,
):
    page = 1
    per_page = 2
    filter_value = created_multiple_product[0]["name"]
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}&name={filter_value}"
    )

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == 1
    assert response.json()["results"][0]["name"] == filter_value
    assert len(response.json()["results"]) == 1


@pytest.mark.anyio
async def test_multiply_filter_products(
    async_client: AsyncClient,
    created_multiple_product: list,
):
    page = 1
    per_page = 2
    filter_name_value = created_multiple_product[0]["name"]
    filter_description_value = created_multiple_product[0]["description"]
    filter_price_value = created_multiple_product[0]["price"]
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}&name={filter_name_value}&description={filter_description_value}&price={filter_price_value}"
    )

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == 1
    assert response.json()["results"][0]["name"] == filter_name_value
    assert response.json()["results"][0]["description"] == filter_description_value
    assert response.json()["results"][0]["price"] == filter_price_value
    assert len(response.json()["results"]) == 1


@pytest.mark.anyio
async def test_asc_sort_name_products(
    async_client: AsyncClient,
    created_multiple_product: list,
    created_multiple_category: list,
):
    page = 1
    per_page = 2
    sort_value = "name"
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}&sort={sort_value}"
    )
    start_index = (page - 1) * per_page
    for i in range(len(created_multiple_product)):
        created_multiple_product[i]["category_name"] = created_multiple_category[
            start_index + i
        ]["name"]
        del created_multiple_product[i]["category_id"]
    fetched_products = sorted(
        created_multiple_product,
        key=lambda x: x["name"],
    )[start_index : page * per_page]

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == 6
    assert response.json()["results"] == fetched_products


@pytest.mark.anyio
async def test_desc_sort_name_products(
    async_client: AsyncClient,
    created_multiple_product: list,
    created_multiple_category: list,
):
    page = 1
    per_page = 2
    sort_value = "-name"
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}&sort={sort_value}"
    )
    start_index = (page - 1) * per_page

    for i in range(len(created_multiple_product)):
        created_multiple_product[i]["category_name"] = created_multiple_category[
            start_index + i
        ]["name"]
        del created_multiple_product[i]["category_id"]
    fetched_products = sorted(
        created_multiple_product, key=lambda x: x["name"], reverse=True
    )[start_index : page * per_page]

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == 6
    assert response.json()["results"] == fetched_products


@pytest.mark.anyio
async def test_asc_sort_price_products(
    async_client: AsyncClient,
    created_multiple_product: list,
    created_multiple_category: list,
):
    page = 1
    per_page = 2
    sort_value = "price"
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}&sort={sort_value}"
    )
    start_index = (page - 1) * per_page
    for i in range(len(created_multiple_product)):
        created_multiple_product[i]["category_name"] = created_multiple_category[
            start_index + i
        ]["name"]
        del created_multiple_product[i]["category_id"]
    fetched_products = sorted(
        created_multiple_product,
        key=lambda x: x["price"],
    )[start_index : page * per_page]

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == 6
    assert response.json()["results"] == fetched_products


@pytest.mark.anyio
async def test_desc_sort_price_products(
    async_client: AsyncClient,
    created_multiple_product: list,
    created_multiple_category: list,
):
    page = 1
    per_page = 2
    sort_value = "-price"
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}&sort={sort_value}"
    )
    start_index = (page - 1) * per_page

    for i in range(len(created_multiple_product)):
        created_multiple_product[i]["category_name"] = created_multiple_category[
            start_index + i
        ]["name"]
        del created_multiple_product[i]["category_id"]
    fetched_products = sorted(
        created_multiple_product, key=lambda x: x["price"], reverse=True
    )[start_index : page * per_page]

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == 6
    assert response.json()["results"] == fetched_products


@pytest.mark.anyio
async def test_not_existing_sort_field_products(
    async_client: AsyncClient,
):
    page = 1
    per_page = 2
    sort_value = "description"
    response = await async_client.get(
        f"/product/product?page={page}&per_page={per_page}&sort={sort_value}"
    )

    assert response.status_code == 422
