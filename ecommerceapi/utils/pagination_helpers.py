import logging
from typing import Type

import sqlalchemy
from databases import Database
from fastapi import Request
from pydantic import BaseModel
from sqlalchemy import Table

from ecommerceapi.models.pagination import PaginatedResponse


async def paginate(
    request: Request,
    page: int,
    per_page: int,
    table: Table,
    logger: logging.Logger,
    db: Database,
    path: str,
    Schema: Type[BaseModel],
) -> PaginatedResponse:
    pass

    logger.info("Getting all categories")

    offset = (page - 1) * per_page
    query = table.select().limit(per_page).offset(offset)
    items = await db.fetch_all(query)
    count_query = sqlalchemy.select(sqlalchemy.func.count()).select_from(table)
    total = await db.fetch_one(count_query)
    base_url = str(request.base_url)
    print(base_url)
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
        results=[Schema(**item) for item in items],
    )
