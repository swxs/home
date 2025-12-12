# -*- coding: utf-8 -*-
# @File    : repositories/oauth_authorization_code_repository.py
# @AUTH    : code_creater

from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.oauth_authorization_code import OAuthAuthorizationCode


class OAuthAuthorizationCodeRepository(BaseRepository[OAuthAuthorizationCode]):
    """
    OAuth授权码Repository
    """

    name = "oauth_authorization_code"
