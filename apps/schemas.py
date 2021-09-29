from typing import Optional, List

from pydantic import BaseModel




class Pager(BaseModel):
    pager: Optional[bool] = True
    page: Optional[int] = 1
    per_page: Optional[int] = 20


class Filter(BaseModel):
    orderby: List[Optional[str]] = []
    filter_: List[Optional[str]] = []
