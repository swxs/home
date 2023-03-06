from typing import List, Optional

import pydantic
from fastapi import Query
from pydantic import BaseModel


class PageSchema(pydantic.BaseModel):
    limit: int = 20
    skip: int = 0


async def get_pagination(
    use_pager: Optional[int] = Query(1),
    limit: Optional[int] = Query(20),
    skip: Optional[int] = Query(0),
    orderby: Optional[str] = Query(...),
):
    if use_pager == 0:
        return PageSchema(**{"limit": 0, "skip": 0})
    else:
        return PageSchema(**{"limit": limit, "skip": skip})
