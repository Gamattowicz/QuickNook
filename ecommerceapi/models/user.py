from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    client = "client"
    seller = "seller"


class User(BaseModel):
    id: int | None = None
    email: str
    role: UserRole = UserRole.client


class UserIn(User):
    password: str
