import logging
from datetime import datetime as dt
from datetime import timedelta
from decimal import Decimal
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import join
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.sql import select

from ecommerceapi.database import database, order_item_table, order_table, product_table
from ecommerceapi.models.order import Order, OrderIn

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", response_model=Order, status_code=201)
async def create_order(order_in: OrderIn):
    try:
        async with database.transaction():
            logger.info("Creating order")
            product_ids = [product.product_id for product in order_in.products]
            # logger.debug(product_ids)

            products_query = select(product_table.c.id, product_table.c.price).where(
                product_table.c.id.in_(product_ids)
            )
            logger.debug(products_query)

            products = await database.fetch_all(products_query)
            # logger.debug(products)

            existing_product_ids = {product.id for product in products}
            # logger.debug(existing_product_ids)

            missing_products = [
                missing_products_id
                for missing_products_id in product_ids
                if missing_products_id not in existing_product_ids
            ]
            # logger.debug(missing_products)

            if missing_products:
                missing_products_str = ", ".join(
                    str(missing_products_id) for missing_products_id in missing_products
                )
                logger.error(f"Products not found with id: {missing_products_str}")
                raise HTTPException(
                    status_code=404,
                    detail=f"Products not found: {missing_products_str}",
                )

            current_time = dt.utcnow()
            payment_due_date = current_time + timedelta(days=5)

            order_values = {
                "delivery_address": order_in.delivery_address,
                "order_date": current_time,
                "payment_due_date": payment_due_date,
                "customer_id": 1,
            }
            # logger.debug(order_values)

            new_order_id = await database.execute(
                order_table.insert().values(order_values)
            )
            # logger.debug(new_order_id)

            total_price = Decimal("0.00")
            # logger.debug(order_in.products)
            order_items_data = []

            for product in order_in.products:
                product_id = product.product_id
                quantity = product.quantity

                product_price_str = next(
                    (p.price for p in products if p.id == product_id), "0.00"
                )
                product_price = Decimal(product_price_str)
                total_price += product_price * quantity

                order_items_data.append(
                    {
                        "order_id": new_order_id,
                        "product_id": product_id,
                        "quantity": quantity,
                    }
                )

            await database.execute_many(order_item_table.insert(), order_items_data)

            await database.execute(
                order_table.update()
                .where(order_table.c.id == new_order_id)
                .values(total_price=str(total_price))
            )

            order_response = {
                "id": new_order_id,
                "order_date": current_time,
                "payment_due_date": payment_due_date,
                "total_price": str(total_price),
                "customer_id": 1,
                "products": [product.model_dump() for product in order_in.products],
                "delivery_address": order_in.delivery_address,
            }

            # logger.debug(order_response)

            return order_response

    except IntegrityError as e:
        logger.error(f"Integrity error: {e}")
        raise HTTPException(
            status_code=400,
            detail="Data integrity error. Make sure the data is correct.",
        )

    except DBAPIError as e:
        logger.error(f"Database API error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed.")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/orders", response_model=List[Order])
async def get_all_orders():
    try:
        logger.info("Getting all orders")

        orders_items_join = join(
            order_table,
            order_item_table,
            order_table.c.id == order_item_table.c.order_id,
        )
        # logger.debug(orders_items_join)
        query = select(
            order_table.c.id,
            order_table.c.delivery_address,
            order_table.c.order_date,
            order_table.c.payment_due_date,
            order_table.c.total_price,
            order_table.c.customer_id,
            order_item_table.c.product_id,
            order_item_table.c.quantity,
        ).select_from(orders_items_join)
        logger.debug(query)
        results = await database.fetch_all(query)
        # logger.debug(results)
        orders_with_products = {}
        for result in results:
            order_id = result.id
            if order_id not in orders_with_products:
                orders_with_products[order_id] = {
                    "id": order_id,
                    "delivery_address": result.delivery_address,
                    "order_date": result.order_date,
                    "payment_due_date": result.payment_due_date,
                    "total_price": str(result.total_price),
                    "customer_id": result.customer_id,
                    "products": [],
                }

            orders_with_products[order_id]["products"].append(
                {"product_id": result.product_id, "quantity": result.quantity}
            )
        # logger.debug(list(orders_with_products.values()))
        return list(orders_with_products.values())

    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while accessing the database."
        )
