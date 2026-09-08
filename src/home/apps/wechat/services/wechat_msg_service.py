# -*- coding: utf-8 -*-
# @File    : services/wechat_msg_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict, Optional

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from home.web.dependencies.session import get_session, transaction

from home.web.exceptions import Http400BadRequestException
from home.web.schemas.pagination import PageSchema

# 本模块方法
from ..repositories.wechat_msg_repository import WechatMsgRepository
from ..schemas.wechat_msg import (
    WechatMsgCreate,
    WechatMsgFilter,
    WechatMsgOut,
    WechatMsgUpdate,
)

logger = logging.getLogger("main.apps.wechat.services.wechat_msg_service")


class WechatMsgService:
    """微信消息记录业务层：CRUD 编排与事务边界。"""

    def __init__(self, session: AsyncSession, repo: Optional[WechatMsgRepository] = None):
        self.session = session
        self.repo = repo or WechatMsgRepository(session)

    async def list(self, filter_schema: WechatMsgFilter, page_schema: PageSchema) -> Dict[str, Any]:
        result = await self.repo.search(filter_schema, page_schema)

        return {
            "data": [WechatMsgOut.model_validate(wm) for wm in result["data"]],
            "pagination": result["pagination"],
        }

    async def get(self, wechat_msg_id: str) -> WechatMsgOut:
        wechat_msg = await self.repo.find_one(wechat_msg_id)

        if wechat_msg is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

        return WechatMsgOut.model_validate(wechat_msg)

    async def create(self, schema: WechatMsgCreate) -> WechatMsgOut:
        async with transaction(self.session):
            wechat_msg = await self.repo.create_one(schema)

        return WechatMsgOut.model_validate(wechat_msg)

    async def update(self, wechat_msg_id: str, schema: WechatMsgUpdate) -> WechatMsgOut:
        async with transaction(self.session):
            wechat_msg = await self.repo.update_one(wechat_msg_id, schema)

        return WechatMsgOut.model_validate(wechat_msg)

    async def delete(self, wechat_msg_id: str) -> int:
        async with transaction(self.session):
            count = await self.repo.delete_one(wechat_msg_id)

        return count


async def get_wechat_msg_service(session: AsyncSession = Depends(get_session)) -> WechatMsgService:
    return WechatMsgService(session)
