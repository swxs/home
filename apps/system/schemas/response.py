# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import Dict, List, TypedDict

from web.schemas.pagination import PaginationSchema

# 本模块方法
from .user import UserSchema
from .user_auth import UserAuthSchema


class UserSearchResponse(TypedDict):
    data: List[UserSchema]
    pagination: PaginationSchema


class UserResponse(TypedDict):
    data: UserSchema


class UserAuthSearchResponse(TypedDict):
    data: List[UserAuthSchema]
    pagination: PaginationSchema


class UserAuthResponse(TypedDict):
    data: UserAuthSchema


class UserWithAuthSearchResponse(TypedDict):
    data: List[UserAuthSchema]
    pagination: PaginationSchema


class TokenResponse(TypedDict):
    token: str
    refresh_token: str
