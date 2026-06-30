# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import List, Optional, TypedDict

from web.schemas.pagination import PaginationSchema

# 本模块方法
from .user import UserOut
from .user_auth import UserAuthOut


class UserWithAuthOut(UserOut):
    """User 字段 + 按 ttype 从认证拍平而来的常用字段（聚合查询输出）。"""

    # 由 user_auth 按 ttype 在 repo 层拍平而来，便于前端表格直接取用
    phone: Optional[str] = None
    email: Optional[str] = None


class UserSearchResponse(TypedDict):
    data: List[UserOut]
    pagination: PaginationSchema


class UserResponse(TypedDict):
    data: UserOut


class UserAuthSearchResponse(TypedDict):
    data: List[UserAuthOut]
    pagination: PaginationSchema


class UserAuthResponse(TypedDict):
    data: UserAuthOut


class UserWithAuthSearchResponse(TypedDict):
    data: List[UserWithAuthOut]
    pagination: PaginationSchema


class TokenResponse(TypedDict):
    token: str
    refresh_token: str
