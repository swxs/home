# -*- coding: utf-8 -*-
# @File    : repositories/oauth_user_grant_repository.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import select

from home.mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.oauth_user_grant import OAuthUserGrant
from ..schemas.oauth_user_grant import OAuthUserGrantSchema


class OAuthUserGrantRepository(BaseRepository[OAuthUserGrant]):
    """
    OAuth用户授权记录Repository
    """

    model = OAuthUserGrant
    name = "oauth_user_grant"

    async def find_by_user_client(self, user_id: str, client_id: str) -> Optional[OAuthUserGrant]:
        query = select(OAuthUserGrant).where(
            OAuthUserGrant.user_id == user_id,
            OAuthUserGrant.client_id == client_id,
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def upsert(self, user_id: str, client_id: str, scope: str) -> OAuthUserGrant:
        grant = await self.find_by_user_client(user_id, client_id)
        if grant:
            return await self.update_one(str(grant.id), OAuthUserGrantSchema(scope=scope))
        return await self.create_one(
            OAuthUserGrantSchema(
                user_id=user_id,
                client_id=client_id,
                scope=scope,
            )
        )
