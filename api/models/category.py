from pydantic import BaseModel, ConfigDict


class CategoryIn(BaseModel):
    name: str


class Category(CategoryIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
