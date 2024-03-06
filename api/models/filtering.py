from typing import Optional

from pydantic import BaseModel


class CategoryFilter(BaseModel):
    name: Optional[str] = None


class ProductFilter(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
