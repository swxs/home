# -*- coding: utf-8 -*-
# @File    : repositories/oauth_client_repository.py
# @AUTH    : code_creater

from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.oauth_client import OAuthClient


class OAuthClientRepository(BaseRepository[OAuthClient]):
    """
    OAuth客户端Repository
    """

    name = "oauth_client"
