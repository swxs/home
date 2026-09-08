# -*- coding: utf-8 -*-
# @File    : services/wechat_message_service.py
# @AUTH    : code_creater

import uuid
import logging

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from wechatpy import parse_message
from wechatpy.events import BaseEvent, SubscribeEvent, UnsubscribeEvent
from wechatpy.messages import TextMessage
from wechatpy.replies import TextReply

from home.web.dependencies.db import get_db
from home.web.dependencies.transaction import transaction
from home.web.schemas.token import TokenSchema

from home.apps.system import consts
from home.apps.system.repositories.user_auth_repository import UserAuthRepository
from home.apps.system.repositories.user_repository import UserRepository
from home.apps.system.schemas.user import UserSchema
from home.apps.system.schemas.user_auth import UserAuthSchema

# 本模块方法
from ..messageContent import content_productor
from ..repositories.wechat_msg_repository import WechatMsgRepository
from ..schemas.wechat_msg import WechatMsgCreate

logger = logging.getLogger("main.apps.wechat.services.wechat_message_service")


class WechatMessageService:
    """微信消息业务层：消息持久化、命令回复编排、关注/取关用户绑定（跨 system）与事务边界。

    跨模块多表写：直接持有 system 的 user / user_auth 表级 repo；每个逻辑写在各自的
    transaction(db) 内提交。HTTP 专属逻辑（签名校验、AES 解密/加密、PlainTextResponse
    构造）保留在 api 层。
    """

    def __init__(
        self,
        db: AsyncSession,
        wechat_msg_repo: WechatMsgRepository | None = None,
        user_repo: UserRepository | None = None,
        user_auth_repo: UserAuthRepository | None = None,
    ):
        self.db = db
        self.wechat_msg_repo = wechat_msg_repo or WechatMsgRepository(db)
        self.user_repo = user_repo or UserRepository(db)
        self.user_auth_repo = user_auth_repo or UserAuthRepository(db)

    async def process(self, decrypted_xml, raw_xml, openid, token_schema: TokenSchema) -> str:
        """处理已解密的微信消息，返回未加密的回复 XML 字符串。"""
        msg = parse_message(decrypted_xml)
        logger.info(f"msg: {msg}")

        if isinstance(msg, BaseEvent):
            event = msg.event
        else:
            event = None

        async with transaction(self.db):
            await self.wechat_msg_repo.create_one(
                WechatMsgCreate(
                    msg_id=msg.id,
                    msg_type=msg.type,
                    msg_event=event,
                    msg=raw_xml.decode("utf8"),
                ),
            )

        content = ""

        if isinstance(msg, TextMessage):
            model = content_productor[msg.content](self.db)

            reply = await model.get_reply(msg, token_schema)

            return reply.render()

        elif isinstance(msg, SubscribeEvent):
            try:
                async with transaction(self.db):
                    user_auth = await self.user_auth_repo.find_one_or_none(
                        UserAuthSchema(
                            ttype=consts.UserAuth_Ttype.WECHAT,
                            identifier=openid,
                            credential=openid,
                        )
                    )
                    if user_auth is None:
                        user = await self.user_repo.create_one(
                            UserSchema(
                                username=f"wecht_user_{str(uuid.uuid4())[:6]}",
                            )
                        )
                        user_auth = await self.user_auth_repo.create_one(
                            UserAuthSchema(
                                user_id=user.id,
                                ttype=consts.UserAuth_Ttype.WECHAT,
                                identifier=openid,
                                credential=openid,
                                ifverified=consts.UserAuth_Ifverified.VERIFIED,
                            )
                        )
                    else:
                        await self.user_auth_repo.update_one(
                            user_auth.id,
                            UserAuthSchema(
                                ifverified=consts.UserAuth_Ifverified.VERIFIED,
                            ),
                        )
            except Exception:
                logger.info(f"openid: {openid} 创建用户信息失败！")
        elif isinstance(msg, UnsubscribeEvent):
            try:
                async with transaction(self.db):
                    user_auth = await self.user_auth_repo.find_one_or_none(
                        UserAuthSchema(
                            ttype=consts.UserAuth_Ttype.WECHAT,
                            identifier=openid,
                            credential=openid,
                        )
                    )
                    if user_auth:
                        await self.user_auth_repo.update_one(
                            user_auth.id,
                            UserAuthSchema(
                                ifverified=consts.UserAuth_Ifverified.UNVERIFIED,
                            ),
                        )
            except Exception:
                logger.info(f"openid: {openid} 解绑用户信息失败！")

        reply = TextReply(content=content, message=msg)
        return reply.render()

    async def handle_test(self, msg: str, token_schema: TokenSchema) -> str:
        model = content_productor[msg]

        reply = await model.get_reply(None, token_schema)

        return reply


async def get_wechat_message_service(db: AsyncSession = Depends(get_db)) -> WechatMessageService:
    return WechatMessageService(db)
