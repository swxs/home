# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import Dict, List, TypedDict

from web.schemas.pagination import PaginationSchema

# 本模块方法
from .user import UserOut
from .user_auth import UserAuthOut


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
    data: List[UserAuthOut]
    pagination: PaginationSchema


class TokenResponse(TypedDict):
    token: str
    refresh_token: str
