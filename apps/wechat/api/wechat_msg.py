# -*- coding: utf-8 -*-
# @File    : api/wechat_msg.py
# @AUTH    : code_creater

import logging

from bson import ObjectId
from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.response import success
from web.custom_types import OID
from web.dependencies.token import TokenSchema, get_token
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination

# 本模块方法
from ..dao.wechat_msg import WechatMsg
from ..schemas.wechat_msg import WechatMsgSchema, get_wechat_msg_schema

router = APIRouter()

logger = logging.getLogger("main.apps.wechat.api.wechat_msg")


@router.get("/")
async def get_wechat_msg_list(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_schema: WechatMsgSchema = Depends(get_wechat_msg_schema),
    page_schema: PageSchema = Depends(get_pagination),
):
    wechat_msg_list = (
        await WechatMsg.search(
            searches=wechat_msg_schema.dict(exclude_unset=True),
            skip=page_schema.skip,
            limit=page_schema.limit,
        )
    ).order_by(page_schema.order_by)

    pagination = PaginationSchema(
        total=await WechatMsg.count(
            finds=wechat_msg_schema.dict(exclude_unset=True),
        ),
        order_by=page_schema.order_by,
        use_pager=page_schema.use_pager,
        page=page_schema.page,
        page_number=page_schema.page_number,
    )

    return success(
        {
            "data": await wechat_msg_list.to_dict(),
            "pagination": pagination.dict(),
        }
    )


@router.get("/{wechat_msg_id}")
async def get_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    wechat_msg = await WechatMsg.find_one(
        finds={"id": ObjectId(wechat_msg_id)},
    )

    return success(
        {
            "data": wechat_msg,
        }
    )


@router.post("/")
async def create_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_schema: WechatMsgSchema = Body(...),
):
    wechat_msg = await WechatMsg.create(
        params=wechat_msg_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": wechat_msg,
        }
    )


@router.put("/{wechat_msg_id}")
async def modify_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: OID = Path(..., regex="[0-9a-f]{24}"),
    wechat_msg_schema: WechatMsgSchema = Body(...),
):
    wechat_msg = await WechatMsg.update_one(
        finds={"id": ObjectId(wechat_msg_id)},
        params=wechat_msg_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": wechat_msg,
        }
    )


@router.delete("/{wechat_msg_id}")
async def delete_wechat_msg(
    token_schema: TokenSchema = Depends(get_token),
    wechat_msg_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    count = await WechatMsg.delete_one(
        finds={"id": ObjectId(wechat_msg_id)},
    )

    return success(
        {
            "count": count,
        }
    )
