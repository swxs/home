import math
from typing import List, Optional

import pydantic
from fastapi import Query
from pydantic import BaseModel


class PaginationSchema(pydantic.BaseModel):
    total: int = 0
    count: int = 0
    use_pager: bool = True
    page: int = 1
    page_number: int = 20

    def __init__(self, **data):
        super().__init__(**data)

        self.count = math.ceil(self.total / self.page_number)


class PageSchema(pydantic.BaseModel):
    limit: int = 20
    skip: int = 0
    order_by: List[str] = []
    use_pager: bool = True
    page: int = 1
    page_number: int = 20


async def get_pagination(
    use_pager: int = Query(1),
    page: int = Query(1),
    page_number: int = Query(20),
    order_by: Optional[List[str]] = Query([], alias="order_by[]"),
):
    if use_pager == 0:
        return PageSchema(
            **{
                "limit": 0,
                "skip": 0,
                "order_by": order_by,
                "use_pager": False,
                "page": page,
                "page_number": page_number,
            }
        )
    else:
        return PageSchema(
            **{
                "limit": page_number,
                "skip": (page - 1) * page_number,
                "order_by": order_by,
                "use_pager": True,
                "page": page,
                "page_number": page_number,
            }
        )
