# -*- coding: utf-8 -*-
# @File    : repositories/oauth_authorization_code_repository.py
# @AUTH    : code_creater

from sqlalchemy.ext.asyncio import AsyncSession

from home.mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.oauth_authorization_code import OAuthAuthorizationCode


class OAuthAuthorizationCodeRepository(BaseRepository[OAuthAuthorizationCode]):
    """
    OAuth授权码Repository
    """

    model = OAuthAuthorizationCode
    name = "oauth_authorization_code"
