import logging

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
) -> PaginatedResponse:
    logger.info(f"Getting all {table.name} with pagination")

    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    items = await db.fetch_all(query)
    count_query = sqlalchemy.select([sqlalchemy.func.count()]).select_from(
        query.alias()
    )
    total = await db.fetch_one(count_query)
    base_url = str(request.base_url)

    next_page = (
        f"{base_url}{path}?page={page + 1}&per_page={per_page}"
        if offset + per_page < total[0]
        else None
    )
    prev_page = (
        f"{base_url}{path}?page={page - 1}&per_page={per_page}" if page > 1 else None
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
