# -*- coding: utf-8 -*-
# @File    : api/message.py
# @AUTH    : code_creater

import logging
from typing import Optional

from fastapi import APIRouter, Body, Query
from fastapi.param_functions import Depends
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidAppIdException, InvalidSignatureException
from wechatpy.utils import check_signature

from core import config
from web.response import success
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token, get_token_by_openid

# 本模块方法
from ..schemas.response import WechatMsgTestResponse
from ..schemas.wechat_msg_test import WechatMsgTestSchema
from ..services.wechat_message_service import (
    WechatMessageService,
    get_wechat_message_service,
)

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
    service: WechatMessageService = Depends(get_wechat_message_service),
) -> PlainTextResponse:
    try:
        xml = await request.body()
        logger.info(f"xml: {xml}")
        crypto = WeChatCrypto(config.WECHAT_TOKEN, config.WECHAT_ENCODING_AES_KEY, config.WECHAT_APPID)
        decrypted_xml = crypto.decrypt_message(xml, msg_signature, timestamp, nonce)
    except (InvalidAppIdException, InvalidSignatureException):
        # 处理异常或忽略
        return PlainTextResponse(content="")

    reply_xml = await service.process(decrypted_xml, xml, openid, token_schema)
    encrypted_xml = crypto.encrypt_message(reply_xml, nonce, timestamp)

    return PlainTextResponse(content=encrypted_xml)


@router.post("/test", response_model=SuccessResponse[WechatMsgTestResponse])
async def post_message_test(
    token_schema: TokenSchema = Depends(get_token),
    msg_schema: WechatMsgTestSchema = Body(...),
    service: WechatMessageService = Depends(get_wechat_message_service),
):
    reply = await service.handle_test(msg_schema.msg, token_schema)

    return success(
        {
            "reply": reply,
        }
    )
