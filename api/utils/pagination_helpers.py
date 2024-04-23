import logging
from typing import Any, Optional

import sqlalchemy
from databases import Database
from fastapi import Request
from sqlalchemy import Table

from api.models.pagination import PaginatedResponse

logger = logging.getLogger(__name__)


async def paginate(
    request: Request,
    page: int,
    per_page: int,
    table: Table,
    db: Database,
    path: str,
    query: sqlalchemy.sql.selectable.Select,
    filters: Optional[dict[str, Any]] = {},
    sort: Optional[str] = None,
    total: Optional[tuple] = None,
) -> PaginatedResponse:
    offset = (page - 1) * per_page
    if isinstance(table, sqlalchemy.sql.selectable.Join):
        logger.info(
            f"Getting all {table.left.name} and {table.right.name} with pagination"
        )
        filtered_paginated_query = query
    else:
        logger.info(f"Getting all {table.name} with pagination")
        filtered_paginated_query = query.limit(per_page).offset(offset)

    items = await db.fetch_all(filtered_paginated_query)

    if total is None:
        count_query = sqlalchemy.select(sqlalchemy.func.count()).select_from(
            query.alias()
        )
        total = await db.fetch_one(count_query)

    base_url = str(request.base_url)

    filter_params = "&".join(
        f"&{key}={int(value) if isinstance(value, float) else value}"
        for key, value in filters.items()
    )

    sort_params = f"&sort={sort}" if sort else ""

    next_page = (
        f"{base_url}{path}?page={page + 1}&per_page={per_page}{filter_params}{sort_params}"
        if offset + per_page < total[0]
        else None
    )
    prev_page = (
        f"{base_url}{path}?page={page - 1}&per_page={per_page}{filter_params}{sort_params}"
        if page > 1
        else None
    )

    logger.debug(query)
    return PaginatedResponse(
        page=page,
        per_page=per_page,
        totalItems=total[0],
        nextPageUrl=next_page,
        prevPageUrl=prev_page,
        results=items,
    )
