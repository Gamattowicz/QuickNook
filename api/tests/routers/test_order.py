from typing import List
from urllib.parse import urljoin

import pytest
from httpx import AsyncClient

from api import security


async def create_order(
    delivery_address: str,
    products: List,
    async_client: AsyncClient,
    logged_in_token: str,
) -> dict:
    response = await async_client.post(
        "/order/",
        json={"delivery_address": delivery_address, "products": products},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


@pytest.fixture()
async def created_order(
    async_client: AsyncClient, created_product: dict, logged_in_token: str
):
    return await create_order(
        "1232 Main St, Anytown, AN 12345",
        [{"product_id": created_product["id"], "quantity": 2}],
        async_client,
        logged_in_token,
    )


@pytest.fixture()
async def created_multiple_order(
    async_client: AsyncClient, created_multiple_product: list, logged_in_token: str
):
    orders = []
    for i in range(6):
        order = await create_order(
            f"1232 Main St, Anytown, AN 1234{i}",
            [{"product_id": created_multiple_product[i]["id"], "quantity": 2}],
            async_client,
            logged_in_token,
        )
        orders.append(order)
    return orders


@pytest.mark.anyio
async def test_create_order(
    async_client: AsyncClient,
    created_product: dict,
    confirmed_user: dict,
    logged_in_token: str,
):
    delivery_address = "1232 Main St, Anytown, AN 12345"
    products = [{"product_id": created_product["id"], "quantity": 2}]

    response = await async_client.post(
        "/order/",
        json={"delivery_address": delivery_address, "products": products},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert {
        "id": confirmed_user["id"],
        "delivery_address": delivery_address,
        "products": products,
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_order_expired_token(
    async_client: AsyncClient,
    created_product: dict,
    confirmed_user: dict,
    mocker,
):
    mocker.patch("api.security.access_token_expire_minutes", return_value=-1)
    token = security.create_access_token(
        confirmed_user["email"], confirmed_user["role"]
    )
    delivery_address = "1232 Main St, Anytown, AN 12345"
    products = [{"product_id": created_product["id"], "quantity": 2}]

    response = await async_client.post(
        "/order/",
        json={"delivery_address": delivery_address, "products": products},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_order_missing_data(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/order/", json={}, headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_orders(async_client: AsyncClient, created_order: dict):
    response = await async_client.get("/order/orders")

    assert response.status_code == 200
    assert response.json()["results"] == [created_order]


@pytest.mark.anyio
async def test_get_all_orders_with_pagination_first_page(
    async_client: AsyncClient, created_multiple_order: list
):
    page = 1
    per_page = 2
    total_order = 6
    response = await async_client.get(f"/order/orders?page={page}&per_page={per_page}")

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_order
    assert response.json()["prevPageUrl"] is None
    assert (
        response.json()["results"]
        == created_multiple_order[(page - 1) * per_page : page * per_page]
    )

    # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["nextPageUrl"]
        == f"{base_url}order/orders?page={page + 1}&per_page={per_page}"
    )


@pytest.mark.anyio
async def test_get_all_orders_with_pagination_second_page(
    async_client: AsyncClient, created_multiple_order: list
):
    page = 2
    per_page = 2
    total_order = 6
    response = await async_client.get(f"/order/orders?page={page}&per_page={per_page}")

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_order
    assert (
        response.json()["results"]
        == created_multiple_order[(page - 1) * per_page : page * per_page]
    )

    # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["prevPageUrl"]
        == f"{base_url}order/orders?page={page - 1}&per_page={per_page}"
    )
    assert (
        response.json()["nextPageUrl"]
        == f"{base_url}order/orders?page={page + 1}&per_page={per_page}"
    )


@pytest.mark.anyio
async def test_get_all_orders_with_pagination_last_page(
    async_client: AsyncClient, created_multiple_order: list
):
    page = 3
    per_page = 2
    total_order = 6
    response = await async_client.get(f"/order/orders?page={page}&per_page={per_page}")

    assert response.status_code == 200
    assert response.json()["page"] == page
    assert response.json()["per_page"] == per_page
    assert response.json()["totalItems"] == total_order
    assert response.json()["nextPageUrl"] is None
    assert (
        response.json()["results"]
        == created_multiple_order[(page - 1) * per_page : page * per_page]
    )

    # Get the base URL
    base_url = urljoin(str(response.url), "/")
    assert (
        response.json()["prevPageUrl"]
        == f"{base_url}order/orders?page={page - 1}&per_page={per_page}"
    )
