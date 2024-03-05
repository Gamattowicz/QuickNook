import logging
from typing import Any

from sqlalchemy import Table
from sqlalchemy.sql import Select

logger = logging.getLogger(__name__)


def apply_filters(filters: dict[str, Any], table: Table) -> Select:
    logger.info(f"Getting all {table.name} with filters")

    for key, value in filters.items():
        if value is not None:
            column = getattr(table.c, key)
            query = table.select().where(column == value)
    return query
