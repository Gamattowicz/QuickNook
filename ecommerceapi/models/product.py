from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductIn(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    image: Optional[str] = None


class Product(ProductIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    thumbnail: Optional[str] = None
