# -*- coding: utf-8 -*-
# @FILE    : schemas/password_lock.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, NotRequired, Optional, TypedDict

import pydantic

from web.schemas.pagination import PaginationSchema

# 本模块方法
from .password_lock import PasswordLockSchema


class PasswordLockSearchResponse(TypedDict):
    data: List[PasswordLockSchema]
    pagination: PaginationSchema


class PasswordLockResponse(TypedDict):
    data: PasswordLockSchema


class PasswordResponse(TypedDict):
    password: str
