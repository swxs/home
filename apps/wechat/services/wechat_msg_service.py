# -*- coding: utf-8 -*-
# @File    : services/wechat_msg_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.schemas.pagination import PageSchema

# 本模块方法
from ..models.wechat_msg import WechatMsg
from ..schemas.wechat_msg import (
    WechatMsgCreate,
    WechatMsgFilter,
    WechatMsgOut,
    WechatMsgUpdate,
)

logger = logging.getLogger("main.apps.wechat.services.wechat_msg_service")


class WechatMsgService:
    """微信消息记录业务层：CRUD 编排与事务边界。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, filter_schema: WechatMsgFilter, page_schema: PageSchema) -> Dict[str, Any]:
        single_worker = await get_single_worker(self.db, WechatMsg)
        async with single_worker as worker:
            result = await worker.repository.search(filter_schema, page_schema)

        return {
            "data": [WechatMsgOut.model_validate(wm) for wm in result["data"]],
            "pagination": result["pagination"],
        }

    async def get(self, wechat_msg_id: str) -> WechatMsgOut:
        single_worker = await get_single_worker(self.db, WechatMsg)
        async with single_worker as worker:
            wechat_msg = await worker.repository.find_one(wechat_msg_id)

        if wechat_msg is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

        return WechatMsgOut.model_validate(wechat_msg)

    async def create(self, schema: WechatMsgCreate) -> WechatMsgOut:
        single_worker = await get_single_worker(self.db, WechatMsg)
        async with single_worker as worker:
            wechat_msg = await worker.repository.create_one(schema)

        return WechatMsgOut.model_validate(wechat_msg)

    async def update(self, wechat_msg_id: str, schema: WechatMsgUpdate) -> WechatMsgOut:
        single_worker = await get_single_worker(self.db, WechatMsg)
        async with single_worker as worker:
            wechat_msg = await worker.repository.update_one(wechat_msg_id, schema)

        return WechatMsgOut.model_validate(wechat_msg)

    async def delete(self, wechat_msg_id: str) -> int:
        single_worker = await get_single_worker(self.db, WechatMsg)
        async with single_worker as worker:
            count = await worker.repository.delete_one(wechat_msg_id)

        return count


async def get_wechat_msg_service(db: AsyncSession = Depends(get_db)) -> WechatMsgService:
    return WechatMsgService(db)
