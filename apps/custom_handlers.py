# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model

from tornado.web import url
import settings
from web.web import BaseHandler, BaseAuthedHanlder, tokener, refresh_tokener
from web.consts import undefined
from web.result import SuccessData
from web.exceptions import ApiException, Info
from web.decorator.render import render
from common.Helpers.Helper_pagenate import Page

from common.Utils import encrypt_utils
from common.Utils.log_utils import getLogger
from .System.utils.User import User, user_schema
from .System.utils.UserAuth import UserAuth, user_auth_schema


log = getLogger("views/user")


class AuthTokenHandler(BaseHandler):
    @render
    async def post(self):
        ttype = self.arguments.get('ttype')
        identifier = self.arguments.get('identifier')
        credential = self.arguments.get('credential')
        user_auth = await UserAuth.select(ttype=ttype, identifier=identifier, credential=credential)
        # 生成jwt
        token = tokener.encode(
            user_id=str(user_auth.user_id),
        )
        refresh_token = refresh_tokener.encode(
            user_id=str(user_auth.user_id),
        )
        return SuccessData(token=token, refresh_token=refresh_token)


class RefreshTokenHandler(BaseAuthedHanlder):
    @render
    async def post(self):
        user_id = self.tokens.get('user_id')
        # 生成jwt
        token = refresh_tokener.encode(
            user_id=str(user_id),
        )
        return SuccessData(token=token)


URL_MAPPING_LIST = [
    url(r'/api/authorize/token/auth/', AuthTokenHandler, name='authorize_auth_token'),
    url(r'/api/authorize/token/refresh/', RefreshTokenHandler, name='authorize_refresh_token'),
]
