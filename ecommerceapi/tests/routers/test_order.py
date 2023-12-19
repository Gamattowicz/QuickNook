from typing import List

import pytest
from httpx import AsyncClient


async def create_order(
    delivery_address: str, products: List, async_client: AsyncClient
) -> dict:
    response = await async_client.post(
        "/order/", json={"delivery_address": delivery_address, "products": products}
    )
    return response.json()


@pytest.fixture()
async def created_order(async_client: AsyncClient, created_product: dict):
    return await create_order(
        "1232 Main St, Anytown, AN 12345",
        [{"product_id": created_product["id"], "quantity": 2}],
        async_client,
    )


@pytest.mark.anyio
async def test_create_order(async_client: AsyncClient, created_product: dict):
    delivery_address = "1232 Main St, Anytown, AN 12345"
    products = [{"product_id": created_product["id"], "quantity": 2}]

    response = await async_client.post(
        "/order/", json={"delivery_address": delivery_address, "products": products}
    )

    assert response.status_code == 201
    assert {
        "id": 1,
        "delivery_address": delivery_address,
        "products": products,
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_order_missing_data(async_client: AsyncClient):
    response = await async_client.post("/order/", json={})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_orders(async_client: AsyncClient, created_order: dict):
    response = await async_client.get("/order/orders")

    assert response.status_code == 200
    assert response.json() == [created_order]
