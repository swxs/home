# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import List, TypedDict

from home.web.schemas.pagination import PaginationSchema

# 本模块方法
from .password_lock import PasswordLockOut


class PasswordLockSearchResponse(TypedDict):
    data: List[PasswordLockOut]
    pagination: PaginationSchema


class PasswordLockResponse(TypedDict):
    data: PasswordLockOut


class PasswordResponse(TypedDict):
    password: str
