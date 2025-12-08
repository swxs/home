# -*- coding: utf-8 -*-
# @File    : repositories/__init__.py
# @AUTH    : code_creater

# 本模块方法
from .user_auth_repository import UserAuthRepository
from .user_repository import UserRepository

__all__ = ["UserRepository", "UserAuthRepository"]
