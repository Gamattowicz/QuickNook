from urllib.parse import urljoin

import pytest
from httpx import AsyncClient

from api import security

# async def create_category(
#     name: str, async_client: AsyncClient, logged_in_token: str
# ) -> dict:
#     response = await async_client.post(
#         "/category/",
#         json={"name": name},
#         headers={"Authorization": f"Bearer {logged_in_token}"},
#     )
#     return response.json()


# @pytest.fixture()
# async def created_category(async_client: AsyncClient, logged_in_token: str):
#     return await create_category("Test Category", async_client, logged_in_token)


@pytest.mark.anyio
async def test_create_category(async_client: AsyncClient, logged_in_token: str):
    name = "TestCategory"

    response = await async_client.post(
        "/category/",
        json={"name": name},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert {"id": 1, "name": name}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_category_expired_token(
    async_client: AsyncClient, confirmed_user: dict, mocker
):
    mocker.patch("api.security.access_token_expire_minutes", return_value=-1)
    token = security.create_access_token(
        confirmed_user["email"], confirmed_user["role"]
    )
    response = await async_client.post(
        "/category/",
        json={"name": "Test Category"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_category_missing_data(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/category/",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_categories(async_client: AsyncClient, created_category: dict):
    response = await async_client.get("/category/category")

    assert response.status_code == 200
    assert response.json()["results"] == [created_category]


@pytest.mark.anyio
async def test_get_all_categories_with_pagination_first_page(
    async_client: AsyncClient, created_multiple_category: list
):
    page = 1
    per_page = 2
    total_category = 6
    response = await async_client.get(
        f"/category/category?page={page}&per_page={per_page}"
    )

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_category
    assert response.json()["prevPageUrl"] is None
    assert (
        response.json()["results"]
        == created_multiple_category[(page - 1) * per_page : page * per_page]
    )

    # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["nextPageUrl"]
        == f"{base_url}category/category?page={page + 1}&per_page={per_page}"
    )


@pytest.mark.anyio
async def test_get_all_categories_with_pagination_second_page(
    async_client: AsyncClient, created_multiple_category: list
):
    page = 2
    per_page = 2
    total_category = 6
    response = await async_client.get(
        f"/category/category?page={page}&per_page={per_page}"
    )

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_category
    assert (
        response.json()["results"]
        == created_multiple_category[(page - 1) * per_page : page * per_page]
    )

    # # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["prevPageUrl"]
        == f"{base_url}category/category?page={page - 1}&per_page={per_page}"
    )
    assert (
        response.json()["nextPageUrl"]
        == f"{base_url}category/category?page={page + 1}&per_page={per_page}"
    )


@pytest.mark.anyio
async def test_get_all_categories_with_pagination_last_page(
    async_client: AsyncClient, created_multiple_category: list
):
    page = 3
    per_page = 2
    total_category = 6
    response = await async_client.get(
        f"/category/category?page={page}&per_page={per_page}"
    )

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_category
    assert response.json()["nextPageUrl"] is None
    assert (
        response.json()["results"]
        == created_multiple_category[(page - 1) * per_page : page * per_page]
    )

    # # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["prevPageUrl"]
        == f"{base_url}category/category?page={page - 1}&per_page={per_page}"
    )


@pytest.mark.anyio
async def test_filter_name_categories(
    async_client: AsyncClient, created_category: dict
):
    page = 1
    per_page = 2
    filter_value = created_category["name"]
    response = await async_client.get(
        f"/category/category?page={page}&per_page={per_page}&name={filter_value}"
    )

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == 1
    assert response.json()["results"][0]["name"] == filter_value
    assert len(response.json()["results"]) == 1
