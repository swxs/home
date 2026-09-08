# -*- coding: utf-8 -*-
# @File    : repositories/oauth_client_repository.py
# @AUTH    : code_creater

from sqlalchemy.ext.asyncio import AsyncSession

from home.mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.oauth_client import OAuthClient


class OAuthClientRepository(BaseRepository[OAuthClient]):
    """
    OAuth客户端Repository
    """

    model = OAuthClient
    name = "oauth_client"

    filterable_fields = {"client_id", "client_name", "redirect_uri", "user_id", "is_active"}
    # client_secret 为敏感字段，不开放排序
    sortable_fields = {"id", "create_at", "update_at", "client_name", "is_active"}
