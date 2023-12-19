import pytest
from httpx import AsyncClient

# async def create_product(
#     name: str,
#     description: str,
#     price: float,
#     category_id: int,
#     async_client: AsyncClient,
# ) -> dict:
#     response = await async_client.post(
#         "/product/",
#         json={
#             "name": name,
#             "description": description,
#             "price": price,
#             "category_id": category_id,
#         },
#     )
#     return response.json()


# @pytest.fixture()
# async def created_product(async_client: AsyncClient, created_category: dict):
#     return await create_product(
#         "Test Product",
#         "Test Description",
#         4.00,
#         created_category["id"],
#         async_client,
#     )


@pytest.mark.anyio
async def test_create_product(async_client: AsyncClient, created_category: dict):
    name = "Test Product"
    description = "Test Description"
    price = 4.00

    response = await async_client.post(
        "/product/",
        json={
            "name": name,
            "description": description,
            "price": price,
            "category_id": created_category["id"],
        },
    )

    assert response.status_code == 201
    assert {
        "id": 1,
        "name": name,
        "description": description,
        "price": price,
        "category_id": created_category["id"],
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
