# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """通用成功响应模型"""

    code: int = 0
    message: str = ""
    data: Optional[T] = None


class SearchResponse(BaseModel, Generic[T]):
    """搜索响应模型（带分页）"""

    code: int = 0
    message: str = ""
    data: Optional[T] = None
