import os
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, Request, Response

os.environ["ENV_STATE"] = "test"
from api.database import database, user_table  # noqa: E402
from api.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.com", "password": "123456", "role": "client"}
    await async_client.post("/user/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details


@pytest.fixture()
async def confirmed_user(registered_user: dict) -> dict:
    query = (
        user_table.update()
        .where(user_table.c.email == registered_user["email"])
        .values(confirmed=True)
    )
    await database.execute(query)
    return registered_user


@pytest.fixture()
async def logged_in_token(async_client: AsyncClient, confirmed_user: dict) -> str:
    response = await async_client.post("/user/token", json=confirmed_user)
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def mock_httpx_client(mocker):
    mocked_client = mocker.patch("api.tasks.httpx.AsyncClient")

    mocked_async_client = Mock()
    response = Response(status_code=200, content="", request=Request("POST", "//"))
    mocked_async_client.post = AsyncMock(return_value=response)
    mocked_client.return_value.__aenter__.return_value = mocked_async_client

    return mocked_async_client


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


@pytest.fixture()
async def created_multiple_category(async_client: AsyncClient, logged_in_token: str):
    categories = []
    for i in range(6):
        category = await create_category(
            f"Test Category {i}", async_client, logged_in_token
        )
        categories.append(category)
    return categories


async def create_product(
    name: str,
    description: str,
    price: float,
    category_id: int,
    async_client: AsyncClient,
) -> dict:
    form_data = {
        "name": (None, name),
        "description": (None, description),
        "price": (None, str(price)),
        "category_id": (None, str(category_id)),
    }
    response = await async_client.post("/product/", files=form_data)
    return response.json()


@pytest.fixture()
async def created_product(async_client: AsyncClient, created_category: dict):
    return await create_product(
        "Test Product",
        "Test Description",
        4.00,
        created_category["id"],
        async_client,
    )


@pytest.fixture()
async def created_multiple_product(
    async_client: AsyncClient, created_multiple_category: list
):
    products = []
    for i in range(6):
        product = await create_product(
            f"Test Product {i}",
            f"Test Description {i}",
            4.00,
            created_multiple_category[i]["id"],
            async_client,
        )
        products.append(product)
    return products
