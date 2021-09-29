from typing import Optional, List

from pydantic import BaseModel
from fastapi import Query

from . import schemas


async def get_pager(
    pager: Optional[bool] = Query(True),
    page: Optional[int] = Query(1),
    per_page: Optional[int] = Query(20),
):
    return schemas.Pager(pager=pager, page=page, per_page=per_page)


async def get_filter(
    orderby: List[Optional[str]] = Query([]),
    filter: List[Optional[str]] = Query([]),
):
    return schemas.Filter(orderby=orderby, filter=filter)
