import pytest
from httpx import AsyncClient

from ecommerceapi import security


async def create_category(
    name: str, async_client: AsyncClient, logged_in_token: str
) -> dict:
    response = await async_client.post(
        "/category/",
        json={"name": name},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


@pytest.fixture()
async def created_category(async_client: AsyncClient, logged_in_token: str):
    return await create_category("Test Category", async_client, logged_in_token)


@pytest.mark.anyio
async def test_create_category(async_client: AsyncClient, logged_in_token: str):
    name = "Test Category"

    response = await async_client.post(
        "/category/",
        json={"name": name},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert {"id": 1, "name": name}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_category_expired_token(
    async_client: AsyncClient, registered_user: dict, mocker
):
    mocker.patch("ecommerceapi.security.access_token_expire_minutes", return_value=-1)
    token = security.create_access_token(registered_user["email"])
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
    assert response.json() == [created_category]
