# -*- coding: utf-8 -*-
# @File    : api/oauth_client.py
# @AUTH    : code_creater

import uuid
import logging
import secrets

from fastapi import APIRouter, Body, Path
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import CountResponse, SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..models.oauth_client import OAuthClient
from ..repositories.oauth_client_repository import OAuthClientRepository
from ..schemas.oauth_client import (
    OAuthClientCreateSchema,
    OAuthClientResponseSchema,
    OAuthClientSchema,
    get_oauth_client_schema,
)

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.oauth_client")


def generate_client_id() -> str:
    """生成客户端ID"""
    return f"client_{uuid.uuid4().hex[:16]}"


def generate_client_secret() -> str:
    """生成客户端密钥（32字节的随机字符串）"""
    return secrets.token_urlsafe(32)


@router.get("/", response_model=SuccessResponse)
async def get_oauth_client_list(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_schema: OAuthClientSchema = Depends(get_oauth_client_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    """获取OAuth客户端列表"""
    single_worker = await get_single_worker(db, OAuthClient)
    async with single_worker as worker:
        result = await worker.repository.search(oauth_client_schema, page_schema)

    # 转换为 Schema，不返回client_secret
    data = []
    for client in result["data"]:
        client_dict = OAuthClientSchema.model_validate(client).model_dump()
        # 移除client_secret，不返回给客户端
        client_dict.pop("client_secret", None)
        data.append(client_dict)

    return success(
        {
            "data": data,
            "pagination": result["pagination"],
        }
    )


@router.get("/{oauth_client_id}", response_model=SuccessResponse)
async def get_oauth_client(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    """获取单个OAuth客户端信息（不返回client_secret）"""
    single_worker = await get_single_worker(db, OAuthClient)
    async with single_worker as worker:
        oauth_client = await worker.repository.find_one(oauth_client_id)

    if oauth_client is None:
        raise Http400BadRequestException(Http400BadRequestException.NoResource, "OAuth客户端不存在")

    # 转换为 Schema，不返回client_secret
    client_dict = OAuthClientSchema.model_validate(oauth_client).model_dump()
    client_dict.pop("client_secret", None)

    return success(
        {
            "data": client_dict,
        }
    )


@router.post("/", response_model=SuccessResponse)
async def create_oauth_client(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_create_schema: OAuthClientCreateSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """创建OAuth客户端"""
    single_worker = await get_single_worker(db, OAuthClient)
    async with single_worker as worker:
        # 生成client_id和client_secret
        client_id = generate_client_id()
        client_secret = generate_client_secret()

        # 检查client_id是否已存在（理论上不会，但为了安全）
        existing_client = await worker.repository.find_one_or_none(OAuthClientSchema(client_id=client_id))
        if existing_client:
            # 如果冲突，重新生成
            client_id = generate_client_id()

        # 创建客户端Schema
        oauth_client_schema = OAuthClientSchema(
            client_id=client_id,
            client_secret=client_secret,
            client_name=oauth_client_create_schema.client_name,
            redirect_uri=oauth_client_create_schema.redirect_uri,
            user_id=oauth_client_create_schema.user_id or token_schema.user_id,
        )

        oauth_client = await worker.repository.create_one(oauth_client_schema)

    # 返回包含client_secret的响应（仅在创建时返回一次）
    response_data = OAuthClientResponseSchema.model_validate(oauth_client).model_dump()

    logger.info(f"创建OAuth客户端: {client_id}, 用户: {token_schema.user_id}")

    return success(
        {
            "data": response_data,
        }
    )


@router.put("/{oauth_client_id}", response_model=SuccessResponse)
async def modify_oauth_client(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    oauth_client_schema: OAuthClientSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """更新OAuth客户端信息（不允许更新client_id和client_secret）"""
    single_worker = await get_single_worker(db, OAuthClient)
    async with single_worker as worker:
        # 检查客户端是否存在
        existing_client = await worker.repository.find_one(oauth_client_id)
        if existing_client is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "OAuth客户端不存在")

        # 移除不允许更新的字段
        update_data = oauth_client_schema.model_dump(exclude_unset=True)
        update_data.pop("client_id", None)
        update_data.pop("client_secret", None)
        update_data.pop("id", None)

        # 创建更新用的Schema
        update_schema = OAuthClientSchema(**update_data)

        oauth_client = await worker.repository.update_one(oauth_client_id, update_schema)

    # 转换为 Schema，不返回client_secret
    client_dict = OAuthClientSchema.model_validate(oauth_client).model_dump()
    client_dict.pop("client_secret", None)

    return success(
        {
            "data": client_dict,
        }
    )


@router.delete("/{oauth_client_id}", response_model=SuccessResponse[CountResponse])
async def delete_oauth_client(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    """删除OAuth客户端"""
    single_worker = await get_single_worker(db, OAuthClient)
    async with single_worker as worker:
        count = await worker.repository.delete_one(oauth_client_id)

    logger.info(f"删除OAuth客户端: {oauth_client_id}, 用户: {token_schema.user_id}")

    return success(
        {
            "count": count,
        }
    )


@router.post("/regenerate-secret/{oauth_client_id}", response_model=SuccessResponse)
async def regenerate_client_secret(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    """重新生成客户端密钥"""
    single_worker = await get_single_worker(db, OAuthClient)
    async with single_worker as worker:
        # 检查客户端是否存在
        existing_client = await worker.repository.find_one(oauth_client_id)
        if existing_client is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "OAuth客户端不存在")

        # 生成新的client_secret
        new_client_secret = generate_client_secret()

        # 更新client_secret
        update_schema = OAuthClientSchema(client_secret=new_client_secret)
        oauth_client = await worker.repository.update_one(oauth_client_id, update_schema)

    # 返回新的client_secret（仅在重新生成时返回一次）
    response_data = OAuthClientResponseSchema.model_validate(oauth_client).model_dump()

    logger.info(f"重新生成OAuth客户端密钥: {oauth_client_id}, 用户: {token_schema.user_id}")

    return success(
        {
            "data": response_data,
        }
    )
