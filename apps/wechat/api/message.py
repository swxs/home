# -*- coding: utf-8 -*-
# @File    : api/wechat_msg.py
# @AUTH    : code_creater

import logging
from typing import Dict, List, Optional

from bson import ObjectId
from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidAppIdException, InvalidSignatureException
from wechatpy.replies import TextReply
from wechatpy.utils import check_signature

from core import config
from web.response import success

router = APIRouter()

logger = logging.getLogger("main.apps.wechat.api.message")


@router.get("/")
async def get_message(
    request: Request,
    echostr: Optional[str] = Query(None),
    nonce: Optional[str] = Query(None),
    signature: Optional[str] = Query(None),
    timestamp: Optional[str] = Query(None),
):
    # if echostr is not None:
    #     try:
    #         check_signature(config.WECHAT_TOKEN, signature, timestamp, nonce)
    #         return PlainTextResponse(content=echostr)
    #     except InvalidSignatureException:
    #         # 处理异常情况或忽略
    #         return PlainTextResponse(content="")

    if echostr is not None:
        try:
            check_signature(config.WECHAT_TOKEN, signature, timestamp, nonce)
            logger.debug(f"check_signature: {signature}, return: {echostr}")
            return PlainTextResponse(content=echostr)
        except (InvalidAppIdException, InvalidSignatureException) as e:
            logger.exception(e)
            return PlainTextResponse(content="")
    else:
        try:
            xml = await request.body()
            logger.info(f"xml: {xml}")
            crypto = WeChatCrypto(config.WECHAT_TOKEN, config.WECHAT_ENCODING_AES_KEY, config.WECHAT_APPID)
            decrypted_xml = crypto.decrypt_message(xml, signature, timestamp, nonce)
        except (InvalidAppIdException, InvalidSignatureException):
            # 处理异常或忽略
            return PlainTextResponse(content="")

        msg = parse_message(decrypted_xml)
        logger.info(f"msg: {msg}")

        reply = TextReply(content='hello world', message=msg)
        xml = reply.render()

        encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)

        return PlainTextResponse(content=encrypted_xml)
