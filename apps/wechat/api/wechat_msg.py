# -*- coding: utf-8 -*-
# @File    : api/wechat_msg.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.token import TokenSchema, get_token
from web.response import success

# 本模块方法
from ..models.wechat_msg import WechatMsg
from ..schemas.wechat_msg import WechatMsgSchema, get_wechat_msg_schema

router = APIRouter()

logger = logging.getLogger("main.apps.wechat.api.wechat_msg")


@router.get("/")
async def get_wechat_msg_list(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_schema: WechatMsgSchema = Depends(get_wechat_msg_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        result = await worker.repository.search(wechat_msg_schema, page_schema)

    # 转换为 Schema
    wechat_msg_list = [WechatMsgSchema.model_validate(wm).model_dump() for wm in result["data"]]

    return success(
        {
            "data": wechat_msg_list,
            "pagination": result["pagination"].model_dump(),
        }
    )


@router.get("/{wechat_msg_id}")
async def get_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        wechat_msg = await worker.repository.find_one(wechat_msg_id)

    # 转换为 Schema
    wechat_msg_response = WechatMsgSchema.model_validate(wechat_msg)

    return success(
        {
            "data": wechat_msg_response.model_dump(),
        }
    )


@router.post("/")
async def create_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_schema: WechatMsgSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        wechat_msg = await worker.repository.create_one(wechat_msg_schema)

    wechat_msg_response = WechatMsgSchema.model_validate(wechat_msg)

    return success(
        {
            "data": wechat_msg_response.model_dump(),
        }
    )


@router.put("/{wechat_msg_id}")
async def modify_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    wechat_msg_schema: WechatMsgSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, WechatMsg)
    async with single_worker as worker:
        wechat_msg = await worker.repository.update_one(wechat_msg_id, wechat_msg_schema)

    # 转换为 Schema
    wechat_msg_response = WechatMsgSchema.model_validate(wechat_msg)

    return success(
        {
            "data": wechat_msg_response.model_dump(),
        }
    )


@router.delete("/{wechat_msg_id}")
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
