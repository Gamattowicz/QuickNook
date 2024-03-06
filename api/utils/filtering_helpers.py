import logging
from typing import Any

from sqlalchemy import Table, func
from sqlalchemy.sql import Select

logger = logging.getLogger(__name__)


def apply_filters(filters: dict[str, Any], table: Table) -> Select:
    logger.info(f"Getting all {table.name} with filters")

    query = table.select()
    filters_kv_pairs = {}
    for key, value in filters.items():
        if value is not None:
            column = getattr(table.c, key)
            filters_kv_pairs[key] = value
            query = query.where(func.lower(column) == func.lower(value))
    return query, filters_kv_pairs
