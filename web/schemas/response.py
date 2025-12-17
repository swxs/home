# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, List, Optional, TypeVar, TypedDict

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """通用成功响应模型"""

    code: int = 0
    message: str = ""
    data: Optional[T] = None


class CountResponse(TypedDict):
    count: int
