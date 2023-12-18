from datetime import datetime
from typing import List

from pydantic import BaseModel


class ProductQuantity(BaseModel):
    product_id: int
    quantity: int


class OrderIn(BaseModel):
    delivery_address: str
    products: List[ProductQuantity]


class Order(OrderIn):
    id: int
    order_date: datetime
    payment_due_date: datetime
    total_price: str
    customer_id: int


class OrderItemIn(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderItem(OrderItemIn):
    id: int
