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
from .System.utils.Organization import Organization, organization_schema
from .System.utils.User import User, user_schema


log = getLogger("views/user")


class AuthTokenHandler(BaseHandler):
    @render
    async def post(self):
        org_id = self.get_argument('org_id')
        username = self.get_argument('username')
        password = self.get_argument('password')

        if (not org_id) or (not username) or (not password): 
            raise ApiCommonException(CommmonExceptionInfo.ValidateException(message="缺失必要参数"))
        
        user = await User.find(orgID=org_id, userName=user_name, password=password, status=USER_STATUS_ACTIVATED)
        if not user:
            raise ApiCommonException(CommmonExceptionInfo.ValidateException(message="登录信息不正确"))

        current_password = jwt_utils.decrypt(password, user.salt)
        if current_password != user.password:
            raise ApiCommonException(CommmonExceptionInfo.ValidateException(message="登录信息不正确"))

        # 生成jwt
        token = jwt_utils.encode2str(
            key=settings.JWT_SECRET_KEY,
            timeout=settings.JWT_TIMEOUT,
            org_id=str(org_id),
            user_id=str(user.id),
        )
        refresh_token = jwt_utils.encode2str(
            timeout=settings.JWT_REFRESH_TIMEOUT,
            org_id=str(org_id),
            user_id=str(user.id),
        )

        return SuccessData(token=token, refresh_token=refresh_token)


class AuthRefreshTokenHandler(BaseHandler):
    """
    刷新jwt
    """
    @render
    async def post(self):
        org_id = self.token_payload.get('org_id')
        user_id = self.token_payload.get('user_id')

        # 生成jwt
        token = jwt_utils.encode2str(
            key=settings.JWT_SECRET_KEY,
            timeout=settings.JWT_TIMEOUT,
            org_id=str(org_id),
            user_id=str(user_id),
        )
        refresh_token = jwt_utils.encode2str(
            timeout=settings.JWT_REFRESH_TIMEOUT,
            org_id=str(org_id),
            user_id=str(user_id),
        )

        return SuccessData(token=token, refresh_token=refresh_token)


URL_MAPPING_LIST = [
    url(r'/api/authorize/token/', AuthTokenHandler, name='authorize_token'),
    url(r'/api/authorize/token/refresh/', AuthRefreshTokenHandler, name='authorize_token_refresh'),
]
