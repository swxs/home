# -*- coding: utf-8 -*-
# @File    : api/oauth_client.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path
from fastapi.param_functions import Depends

from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import CountResponse, SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.oauth_client import (
    OAuthClientCreateSchema,
    OAuthClientFilter,
    OAuthClientUpdate,
    get_oauth_client_filter,
)
from ..services.oauth_client_service import (
    OAuthClientService,
    get_oauth_client_service,
)

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.oauth_client")


@router.get("/", response_model=SuccessResponse)
async def get_oauth_client_list(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_schema: OAuthClientFilter = Depends(get_oauth_client_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: OAuthClientService = Depends(get_oauth_client_service),
):
    """获取OAuth客户端列表"""
    result = await service.list(oauth_client_schema, page_schema)
    return success(result)


@router.get("/{oauth_client_id}", response_model=SuccessResponse)
async def get_oauth_client(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: OAuthClientService = Depends(get_oauth_client_service),
):
    """获取单个OAuth客户端信息（不返回client_secret）"""
    client_dict = await service.get(oauth_client_id)
    return success({"data": client_dict})


@router.post("/", response_model=SuccessResponse)
async def create_oauth_client(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_create_schema: OAuthClientCreateSchema = Body(...),
    service: OAuthClientService = Depends(get_oauth_client_service),
):
    """创建OAuth客户端"""
    response_data = await service.create(oauth_client_create_schema, token_schema.user_id)
    return success({"data": response_data})


@router.put("/{oauth_client_id}", response_model=SuccessResponse)
async def modify_oauth_client(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    oauth_client_schema: OAuthClientUpdate = Body(...),
    service: OAuthClientService = Depends(get_oauth_client_service),
):
    """更新OAuth客户端信息（不允许更新client_id和client_secret）"""
    client_dict = await service.update(oauth_client_id, oauth_client_schema)
    return success({"data": client_dict})


@router.delete("/{oauth_client_id}", response_model=SuccessResponse[CountResponse])
async def delete_oauth_client(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: OAuthClientService = Depends(get_oauth_client_service),
):
    """删除OAuth客户端"""
    count = await service.delete(oauth_client_id, token_schema.user_id)
    return success({"count": count})


@router.post("/regenerate-secret/{oauth_client_id}", response_model=SuccessResponse)
async def regenerate_client_secret(
    token_schema: TokenSchema = Depends(get_token),
    oauth_client_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: OAuthClientService = Depends(get_oauth_client_service),
):
    """重新生成客户端密钥"""
    response_data = await service.regenerate_secret(oauth_client_id, token_schema.user_id)
    return success({"data": response_data})
