# -*- coding: utf-8 -*-
# @File    : api/wechat_msg.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..models.wechat_msg import WechatMsg
from ..schemas.response import CountResponse, WechatMsgResponse, WechatMsgSearchResponse
from ..schemas.wechat_msg import WechatMsgSchema, get_wechat_msg_schema

router = APIRouter()

logger = logging.getLogger("main.apps.wechat.api.wechat_msg")


@router.get("/", response_model=SuccessResponse[WechatMsgSearchResponse])
async def get_wechat_msg_list(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_schema: WechatMsgSchema = Depends(get_wechat_msg_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        result = await worker.repository.search(wechat_msg_schema, page_schema)

    return success(
        {
            "data": [WechatMsgSchema.model_validate(wm) for wm in result["data"]],
            "pagination": result["pagination"],
        }
    )


@router.get("/{wechat_msg_id}", response_model=SuccessResponse[WechatMsgResponse])
async def get_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        wechat_msg = await worker.repository.find_one(wechat_msg_id)

    if wechat_msg is None:
        raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

    return success(
        {
            "data": WechatMsgSchema.model_validate(wechat_msg),
        }
    )


@router.post("/", response_model=SuccessResponse[WechatMsgResponse])
async def create_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_schema: WechatMsgSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        wechat_msg = await worker.repository.create_one(wechat_msg_schema)

    return success(
        {
            "data": WechatMsgSchema.model_validate(wechat_msg),
        }
    )


@router.put("/{wechat_msg_id}", response_model=SuccessResponse[WechatMsgResponse])
async def modify_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    wechat_msg_schema: WechatMsgSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        wechat_msg = await worker.repository.update_one(wechat_msg_id, wechat_msg_schema)

    return success(
        {
            "data": WechatMsgSchema.model_validate(wechat_msg),
        }
    )


@router.delete("/{wechat_msg_id}", response_model=SuccessResponse[CountResponse])
async def delete_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        count = await worker.repository.delete_one(wechat_msg_id)

    return success(
        {
            "count": count,
        }
    )
