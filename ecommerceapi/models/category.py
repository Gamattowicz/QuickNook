from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str


class Category(CategoryIn):
    id: int
