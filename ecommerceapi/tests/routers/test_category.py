import pytest
from httpx import AsyncClient


async def create_category(name: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/category/", json={"name": name})
    return response.json()


@pytest.fixture()
async def created_category(async_client: AsyncClient):
    return await create_category("Test Category", async_client)


@pytest.mark.anyio
async def test_create_category(async_client: AsyncClient):
    name = "Test Category2"

    response = await async_client.post("/category/", json={"name": name})

    assert response.status_code == 201
    assert {"id": 0, "name": name}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_category_missing_data(async_client: AsyncClient):
    response = await async_client.post("/category/", json={})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_categories(async_client: AsyncClient, created_category: dict):
    response = await async_client.get("/category/category")

    assert response.status_code == 200
    assert response.json() == [created_category]
