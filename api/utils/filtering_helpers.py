import logging
from typing import Any, Union

from sqlalchemy import Table, func, sql
from sqlalchemy.sql import Select

logger = logging.getLogger(__name__)


def apply_filters(
    filters: dict[str, Any], query_source: Union[Table, Select]
) -> Select:
    query = query_source.select()
    if isinstance(query_source, Table):
        logger.info(f"Getting all {query_source.name} with filters")
    elif isinstance(query_source, Select):
        logger.info("Applying filters to Select query")
    filters_kv_pairs = {}
    for key, value in filters.items():
        if value:
            column = getattr(query_source.c, key)
            filters_kv_pairs[key] = value
            query = query.where(func.lower(column) == func.lower(value))
        else:
            query = query.where(sql.false())
    return query, filters_kv_pairs
