# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model

import json
from tornado.web import url
import settings
from web.web import BaseHandler
from web.consts import undefined
from web.result import SuccessData
from web.exceptions import ApiCommonException, CommmonExceptionInfo
from web.decorator.render import render
from common.Helpers.Helper_pagenate import Page
from common.Utils import encrypt_utils
from common.Utils.log_utils import getLogger
from .System.utils.User import User, user_schema


log = getLogger("views/user")


class AuthTokenHandler(BaseHandler):
    @render
    async def post(self):
        user_id = self.arguments.get('user_id')
        # 生成jwt
        token = encrypt_utils.encode2str(
            key=settings.JWT_SECRET_KEY,
            timeout=settings.JWT_TIMEOUT,
            user_id=str(user_id),
        )
        refresh_token = encrypt_utils.encode2str(
            timeout=settings.JWT_REFRESH_TIMEOUT,
            user_id=str(user_id),
        )
        return SuccessData(token=token, refresh_token=refresh_token)


URL_MAPPING_LIST = [
    url(r'/api/authorize/token/', AuthTokenHandler, name='authorize_token'),
]
