# -*- coding: utf-8 -*-
# @File    : api/wechat_msg.py
# @AUTH    : code_creater
#
# 注意：本文件为「未挂载死代码」——其 router 未被 api/__init__.py 引入，对外不可达。
# 已按统一分层范式改造（薄控制器 + WechatMsgService），但仍保持不挂载、对外行为不变。

import logging

from fastapi import APIRouter, Body, Path
from fastapi.param_functions import Depends

from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import CountResponse, SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.response import WechatMsgResponse, WechatMsgSearchResponse
from ..schemas.wechat_msg import (
    WechatMsgCreate,
    WechatMsgFilter,
    WechatMsgUpdate,
    get_wechat_msg_filter,
)
from ..services.wechat_msg_service import WechatMsgService, get_wechat_msg_service

router = APIRouter()

logger = logging.getLogger("main.apps.wechat.api.wechat_msg")


@router.get("/", response_model=SuccessResponse[WechatMsgSearchResponse])
async def get_wechat_msg_list(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_schema: WechatMsgFilter = Depends(get_wechat_msg_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: WechatMsgService = Depends(get_wechat_msg_service),
):
    result = await service.list(wechat_msg_schema, page_schema)
    return success(result)


@router.get("/{wechat_msg_id}", response_model=SuccessResponse[WechatMsgResponse])
async def get_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: WechatMsgService = Depends(get_wechat_msg_service),
):
    wechat_msg = await service.get(wechat_msg_id)
    return success({"data": wechat_msg})


@router.post("/", response_model=SuccessResponse[WechatMsgResponse])
async def create_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_schema: WechatMsgCreate = Body(...),
    service: WechatMsgService = Depends(get_wechat_msg_service),
):
    wechat_msg = await service.create(wechat_msg_schema)
    return success({"data": wechat_msg})


@router.put("/{wechat_msg_id}", response_model=SuccessResponse[WechatMsgResponse])
async def modify_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    wechat_msg_schema: WechatMsgUpdate = Body(...),
    service: WechatMsgService = Depends(get_wechat_msg_service),
):
    wechat_msg = await service.update(wechat_msg_id, wechat_msg_schema)
    return success({"data": wechat_msg})


@router.delete("/{wechat_msg_id}", response_model=SuccessResponse[CountResponse])
async def delete_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: WechatMsgService = Depends(get_wechat_msg_service),
):
    count = await service.delete(wechat_msg_id)
    return success({"count": count})
