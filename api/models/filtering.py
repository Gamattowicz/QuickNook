from typing import Optional

from pydantic import BaseModel


class CategoryFilter(BaseModel):
    name: Optional[str] = None
