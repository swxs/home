from typing import List, Optional

import pydantic
from fastapi import Query
from pydantic import BaseModel


class PageSchema(pydantic.BaseModel):
    limit: int = 20
    skip: int = 0
    order_by: List[str] = []


async def get_pagination(
    use_pager: int = Query(1),
    page: int = Query(1),
    page_number: int = Query(20),
    order_by: Optional[List[str]] = Query([]),
):
    if use_pager == 0:
        return PageSchema(
            **{
                "limit": 0,
                "skip": 0,
                "order_by": order_by,
            }
        )
    else:
        return PageSchema(
            **{
                "limit": page_number,
                "skip": (page - 1) * page_number,
                "order_by": order_by,
            }
        )
