from typing import List

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
    assert response.json() == [created_order]
