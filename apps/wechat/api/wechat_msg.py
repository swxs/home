# -*- coding: utf-8 -*-
# @File    : api/wechat_msg.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.token import TokenSchema, get_token
from web.exceptions import Http400BadRequestException
from web.response import success

# 本模块方法
from ..repositories.wechat_msg_repository import WechatMsgRepository
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
    wechat_msg_repo = WechatMsgRepository(db)

    # 使用Repository搜索方法
    result = await wechat_msg_repo.search(wechat_msg_schema, page_schema)

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
    wechat_msg_repo = WechatMsgRepository(db)

    # 使用Repository查找方法
    wechat_msg = await wechat_msg_repo.find_one(wechat_msg_id, "微信消息不存在")

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
    wechat_msg_repo = WechatMsgRepository(db)

    # 使用Repository创建方法
    wechat_msg = await wechat_msg_repo.create_one(wechat_msg_schema, "微信消息创建失败")

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
    wechat_msg_repo = WechatMsgRepository(db)

    # 使用Repository更新方法
    wechat_msg = await wechat_msg_repo.update_one(
        wechat_msg_id,
        wechat_msg_schema,
        "微信消息不存在",
        "微信消息更新失败",
    )

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
    wechat_msg_repo = WechatMsgRepository(db)

    # 使用Repository删除方法
    count = await wechat_msg_repo.delete_one(wechat_msg_id, "微信消息不存在", "微信消息删除失败")

    return success(
        {
            "count": count,
        }
    )
