# -*- coding: utf-8 -*-
# @File    : api/wechat_msg.py
# @AUTH    : code_creater

import logging
from typing import Dict, List, Optional

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

from apps.system import consts
from apps.system.dao.user_auth import UserAuth
from apps.system.schemas.user_auth import UserAuthSchema
from core import config
from web.dependencies.token import TokenSchema, get_token, get_token_by_openid
from web.response import success

# 本模块方法
from ..dao.wechat_msg import WechatMsg
from ..messageContent import content_productor
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
):
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
):
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

    await WechatMsg.create(
        params=WechatMsgSchema(
            msg_id=msg.id,
            msg_type=msg.type,
            msg_event=event,
            msg=xml.decode("utf8"),
        ).dict(exclude_defaults=True),
    )

    content = ''

    if isinstance(msg, TextMessage):
        model = content_productor[msg.content]

        reply = await model.get_reply(msg, token_schema)

        xml = reply.render()
        encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)

        return PlainTextResponse(content=encrypted_xml)

    elif isinstance(msg, SubscribeEvent):
        try:
            await UserAuth.create(
                params=UserAuthSchema(
                    ttype=consts.USER_AUTH_TTYPE_WECHAT,
                    identifier=openid,
                    credential=openid,
                    ifverified=consts.USER_AUTH_IFVERIFIED_FALSE,
                ).dict(exclude_defaults=True),
            )
        except Exception as e:
            logger.info(f"openid: {openid} 创建用户信息失败！")
            pass
    elif isinstance(msg, UnsubscribeEvent):
        try:
            await UserAuth.update_one(
                finds={
                    "ttype": consts.USER_AUTH_TTYPE_WECHAT,
                    "identifier": openid,
                    "credential": openid,
                },
                params=UserAuthSchema(
                    ifverified=consts.USER_AUTH_IFVERIFIED_FALSE,
                ).dict(exclude_defaults=True),
            )
        except Exception as e:
            logger.info(f"openid: {openid} 解绑用户信息失败！")
            pass

    reply = TextReply(content=content, message=msg)
    xml = reply.render()
    encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)

    return PlainTextResponse(content=encrypted_xml)


@router.post("/test")
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
