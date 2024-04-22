import logging
from typing import Any

from sqlalchemy import desc
from sqlalchemy.sql import Select

logger = logging.getLogger(__name__)


def apply_sorting(sort_field: dict[str, Any], query: Select):
    if sort_field.startswith("-"):
        return query.order_by(desc(sort_field[1:]))
    else:
        return query.order_by(sort_field)
