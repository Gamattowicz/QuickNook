from enum import Enum


class CategorySortOptions(str, Enum):
    name = "name"
    desc_name = "-name"


class ProductSortOptions(str, Enum):
    price = "price"
    name = "name"
    desc_price = "-price"
    desc_name = "-name"
