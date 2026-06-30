# -*- coding: utf-8 -*-
# @File    : services/oauth_client_service.py
# @AUTH    : code_creater

import uuid
import logging
import secrets
from typing import Any, Dict, Optional

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db
from web.dependencies.transaction import transaction
from web.exceptions import Http400BadRequestException
from web.schemas.pagination import PageSchema

# 本模块方法
from ..repositories.oauth_client_repository import OAuthClientRepository
from ..schemas.oauth_client import (
    OAuthClientCreateSchema,
    OAuthClientFilter,
    OAuthClientResponseSchema,
    OAuthClientSchema,
    OAuthClientUpdate,
)

logger = logging.getLogger("main.apps.system.services.oauth_client_service")


def generate_client_id() -> str:
    """生成客户端ID"""
    return f"client_{uuid.uuid4().hex[:16]}"


def generate_client_secret() -> str:
    """生成客户端密钥（32字节的随机字符串）"""
    return secrets.token_urlsafe(32)


class OAuthClientService:
    """OAuth 客户端业务层：CRUD、密钥生成与字段暴露策略、事务边界。"""

    def __init__(self, db: AsyncSession, repo: Optional[OAuthClientRepository] = None):
        self.db = db
        self.repo = repo or OAuthClientRepository(db)

    async def list(self, filter_schema: OAuthClientFilter, page_schema: PageSchema) -> Dict[str, Any]:
        result = await self.repo.search(filter_schema, page_schema)

        # 转换为 Schema，不返回client_secret
        data = []
        for client in result["data"]:
            client_dict = OAuthClientSchema.model_validate(client).model_dump()
            # 移除client_secret，不返回给客户端
            client_dict.pop("client_secret", None)
            data.append(client_dict)

        return {
            "data": data,
            "pagination": result["pagination"],
        }

    async def get(self, oauth_client_id: str) -> Dict[str, Any]:
        oauth_client = await self.repo.find_one(oauth_client_id)

        if oauth_client is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "OAuth客户端不存在")

        # 转换为 Schema，不返回client_secret
        client_dict = OAuthClientSchema.model_validate(oauth_client).model_dump()
        client_dict.pop("client_secret", None)

        return client_dict

    async def create(
        self,
        create_schema: OAuthClientCreateSchema,
        token_user_id: Optional[str],
    ) -> Dict[str, Any]:
        # 生成client_id和client_secret
        client_id = generate_client_id()
        client_secret = generate_client_secret()

        async with transaction(self.db):
            # 检查client_id是否已存在（理论上不会，但为了安全）
            existing_client = await self.repo.find_one_or_none(OAuthClientSchema(client_id=client_id))
            if existing_client:
                # 如果冲突，重新生成
                client_id = generate_client_id()

            # 创建客户端Schema
            oauth_client_schema = OAuthClientSchema(
                client_id=client_id,
                client_secret=client_secret,
                client_name=create_schema.client_name,
                redirect_uri=create_schema.redirect_uri,
                user_id=create_schema.user_id or token_user_id,
            )

            oauth_client = await self.repo.create_one(oauth_client_schema)

        # 返回包含client_secret的响应（仅在创建时返回一次）
        response_data = OAuthClientResponseSchema.model_validate(oauth_client).model_dump()

        logger.info(f"创建OAuth客户端: {client_id}, 用户: {token_user_id}")

        return response_data

    async def update(self, oauth_client_id: str, schema: OAuthClientUpdate) -> Dict[str, Any]:
        # 检查客户端是否存在
        existing_client = await self.repo.find_one(oauth_client_id)
        if existing_client is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "OAuth客户端不存在")

        # 移除不允许更新的字段
        update_data = schema.model_dump(exclude_unset=True)
        update_data.pop("client_id", None)
        update_data.pop("client_secret", None)
        update_data.pop("id", None)

        # 创建更新用的Schema
        update_schema = OAuthClientSchema(**update_data)

        async with transaction(self.db):
            oauth_client = await self.repo.update_one(oauth_client_id, update_schema)

        # 转换为 Schema，不返回client_secret
        client_dict = OAuthClientSchema.model_validate(oauth_client).model_dump()
        client_dict.pop("client_secret", None)

        return client_dict

    async def delete(self, oauth_client_id: str, token_user_id: Optional[str]) -> int:
        async with transaction(self.db):
            count = await self.repo.delete_one(oauth_client_id)

        logger.info(f"删除OAuth客户端: {oauth_client_id}, 用户: {token_user_id}")

        return count

    async def regenerate_secret(self, oauth_client_id: str, token_user_id: Optional[str]) -> Dict[str, Any]:
        # 检查客户端是否存在
        existing_client = await self.repo.find_one(oauth_client_id)
        if existing_client is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "OAuth客户端不存在")

        # 生成新的client_secret
        new_client_secret = generate_client_secret()

        # 更新client_secret
        update_schema = OAuthClientSchema(client_secret=new_client_secret)
        async with transaction(self.db):
            oauth_client = await self.repo.update_one(oauth_client_id, update_schema)

        # 返回新的client_secret（仅在重新生成时返回一次）
        response_data = OAuthClientResponseSchema.model_validate(oauth_client).model_dump()

        logger.info(f"重新生成OAuth客户端密钥: {oauth_client_id}, 用户: {token_user_id}")

        return response_data


async def get_oauth_client_service(db: AsyncSession = Depends(get_db)) -> OAuthClientService:
    return OAuthClientService(db)
