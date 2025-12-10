# -*- coding: utf-8 -*-
# @File    : api/message.py
# @AUTH    : code_creater

import uuid
import logging
from typing import Optional

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.events import BaseEvent, SubscribeEvent, UnsubscribeEvent
from wechatpy.exceptions import InvalidAppIdException, InvalidSignatureException
from wechatpy.messages import BaseMessage, TextMessage
from wechatpy.replies import TextReply
from wechatpy.utils import check_signature

from core import config
from web.dependencies.db import get_unit_worker
from web.dependencies.unit_worker import UnitWorker
from web.response import success
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token, get_token_by_openid

from apps.system import consts
from apps.system.models.user import User
from apps.system.models.user_auth import UserAuth
from apps.system.repositories.user_auth_repository import UserAuthRepository
from apps.system.repositories.user_repository import UserRepository
from apps.system.schemas.user import UserSchema
from apps.system.schemas.user_auth import UserAuthSchema

# 本模块方法
from ..messageContent import content_productor
from ..models.wechat_msg import WechatMsg
from ..repositories.wechat_msg_repository import WechatMsgRepository
from ..schemas.response import WechatMsgTestResponse
from ..schemas.wechat_msg import WechatMsgSchema
from ..schemas.wechat_msg_test import WechatMsgTestSchema

router = APIRouter()

logger = logging.getLogger("main.apps.wechat.api.message")


@router.get("/")
async def get_message(
    echostr: Optional[str] = Query(None),
    nonce: Optional[str] = Query(None),
    signature: Optional[str] = Query(None),
    timestamp: Optional[str] = Query(None),
) -> PlainTextResponse:
    try:
        check_signature(config.WECHAT_TOKEN, signature, timestamp, nonce)
        logger.debug(f"check_signature: {signature}, return: {echostr}")
        return PlainTextResponse(content=echostr)
    except (InvalidAppIdException, InvalidSignatureException) as e:
        logger.exception(e)
        return PlainTextResponse(content="")


@router.post("/")
async def post_message(
    request: Request,
    signature: Optional[str] = Query(None),
    timestamp: Optional[str] = Query(None),
    nonce: Optional[str] = Query(None),
    openid: Optional[str] = Query(None),
    encrypt_type: Optional[str] = Query(None),
    msg_signature: Optional[str] = Query(None),
    token_schema: TokenSchema = Depends(get_token_by_openid),
    unit_worker: UnitWorker = Depends(get_unit_worker),
) -> PlainTextResponse:
    try:
        xml = await request.body()
        logger.info(f"xml: {xml}")
        crypto = WeChatCrypto(config.WECHAT_TOKEN, config.WECHAT_ENCODING_AES_KEY, config.WECHAT_APPID)
        decrypted_xml = crypto.decrypt_message(xml, msg_signature, timestamp, nonce)
    except (InvalidAppIdException, InvalidSignatureException):
        # 处理异常或忽略
        return PlainTextResponse(content="")

    msg = parse_message(decrypted_xml)
    logger.info(f"msg: {msg}")

    if isinstance(msg, BaseEvent):
        event = msg.event
    else:
        event = None

    async with unit_worker as uw:
        wechat_msg_repo: WechatMsgRepository = uw.get_repository(WechatMsg)
        await wechat_msg_repo.create_one(
            WechatMsgSchema(
                msg_id=msg.id,
                msg_type=msg.type,
                msg_event=event,
                msg=xml.decode("utf8"),
            ),
        )

    content = ""

    if isinstance(msg, TextMessage):
        model = content_productor[msg.content](unit_worker.db)

        reply = await model.get_reply(msg, token_schema)

        xml = reply.render()
        encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)

        return PlainTextResponse(content=encrypted_xml)

    elif isinstance(msg, SubscribeEvent):
        try:
            async with unit_worker as uw:
                user_repo: UserRepository = uw.get_repository(User)
                user_auth_repo: UserAuthRepository = uw.get_repository(UserAuth)
                user_auth = await user_auth_repo.find_one_or_none(
                    UserAuthSchema(
                        ttype=consts.UserAuth_Ttype.WECHAT,
                        identifier=openid,
                        credential=openid,
                    )
                )
                if user_auth is None:
                    user = await user_repo.create_one(
                        UserSchema(
                            username=f"wecht_user_{str(uuid.uuid4())[:6]}",
                        )
                    )
                    user_auth = await user_auth_repo.create_one(
                        UserAuthSchema(
                            user_id=user.id,
                            ttype=consts.UserAuth_Ttype.WECHAT,
                            identifier=openid,
                            credential=openid,
                            ifverified=consts.UserAuth_Ifverified.VERIFIED,
                        )
                    )
                else:
                    await user_auth_repo.update_one(
                        user_auth.id,
                        UserAuthSchema(
                            ifverified=consts.UserAuth_Ifverified.VERIFIED,
                        ),
                    )
        except Exception as e:
            logger.info(f"openid: {openid} 创建用户信息失败！")
            pass
    elif isinstance(msg, UnsubscribeEvent):
        try:
            async with unit_worker as uw:
                user_auth_repo: UserAuthRepository = uw.get_repository(UserAuth)
                user_auth = await user_auth_repo.find_one_or_none(
                    UserAuthSchema(
                        ttype=consts.UserAuth_Ttype.WECHAT,
                        identifier=openid,
                        credential=openid,
                    )
                )
            if user_auth:
                await user_auth_repo.update_one(
                    user_auth.id,
                    UserAuthSchema(
                        ifverified=consts.UserAuth_Ifverified.UNVERIFIED,
                    ),
                )
        except Exception as e:
            logger.info(f"openid: {openid} 解绑用户信息失败！")
            pass

    reply = TextReply(content=content, message=msg)
    xml = reply.render()
    encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)

    return PlainTextResponse(content=encrypted_xml)


@router.post("/test", response_model=SuccessResponse[WechatMsgTestResponse])
async def post_message_test(
    token_schema: TokenSchema = Depends(get_token),
    msg_schema: WechatMsgTestSchema = Body(...),
):
    model = content_productor[msg_schema.msg]

    reply = await model.get_reply(None, token_schema)

    return success(
        {
            "reply": reply,
        }
    )
