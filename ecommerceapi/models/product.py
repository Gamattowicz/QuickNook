from pydantic import BaseModel, ConfigDict


class ProductIn(BaseModel):
    name: str
    description: str
    price: float
    category_id: int


class Product(ProductIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
