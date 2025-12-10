from typing import List, Optional

import pydantic
from fastapi import Header, Query
from pydantic import BaseModel

from apps.system import consts


class SearchSchema(pydantic.BaseModel):
    search: Optional[str] = None


async def get_search(
    search: Optional[str] = Query(None),
):
    return SearchSchema(search=search)
