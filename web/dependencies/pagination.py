from typing import Optional, List

from pydantic import BaseModel
from fastapi import Query


async def get_pagination(
    limit: Optional[int] = Query(1),
    skip: Optional[int] = Query(20),
):
    return {"limit": limit, "skip": skip}
