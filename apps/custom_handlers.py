# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model

import logging
from tornado.web import url
import settings
from web import BaseHandler, render, SuccessData, ApiException, ApiUnknowException, Info
from commons.Helpers import tokener, refresh_tokener
from commons.Helpers.Helper_pagenate import Page
from commons.Helpers.Helper_JWT import AuthTokner, InvalidSignatureError, ExpiredSignatureError, ImmatureSignatureError
from .System.utils.User import User, user_schema
from .System.utils.UserAuth import UserAuth, user_auth_schema


logger = logging.getLogger("main.user.custom_handlers")


class UserAuthHandler(BaseHandler):
    @render
    async def post(self):
        creates = user_auth_schema.load(self.arguments).data
        user_auth = await UserAuth.create(creates)
        token = tokener.encode(
            user_id=str(user_auth.user_id),
        )
        refresh_token = refresh_tokener.encode(
            user_id=str(user_auth.user_id),
        )
        return SuccessData(
            user_id=user_auth.user_id,
            id=user_auth.id,
            ttype=user_auth.ttype,
            identifier=user_auth.identifier,
            ifverified=user_auth.ifverified,
            token=token,
            refresh_token=refresh_token,
        )


class AuthTokenHandler(BaseHandler):
    @render
    async def post(self):
        ttype = self.arguments.get('ttype')
        identifier = self.arguments.get('identifier')
        credential = self.arguments.get('credential')
        user_auth = await UserAuth.find(dict(ttype=ttype, identifier=identifier, credential=credential))
        # 生成jwt
        token = tokener.encode(
            user_id=str(user_auth.user_id),
        )
        refresh_token = refresh_tokener.encode(
            user_id=str(user_auth.user_id),
        )
        return SuccessData(token=token, refresh_token=refresh_token)


class RefreshTokenHandler(BaseHandler):
    @render
    async def post(self):
        refresh_token = self.arguments.get('refresh_token')
        try:
            header, payload = refresh_tokener.decode(refresh_token)
            user_id = payload.get('user_id')
        except InvalidSignatureError:
            raise ApiException(Info.TokenIllegal, template='Invalid Token.')
        except ExpiredSignatureError:
            raise ApiException(Info.TokenTimeout, template='Token expire date.')
        except ImmatureSignatureError:
            raise ApiException(Info.TokenIllegal, template='Immature signature.')
        except Exception as e:
            raise ApiUnknowException(e, Info.Base)
        # 生成jwt
        token = refresh_tokener.encode(
            user_id=str(user_id),
        )
        return SuccessData(token=token)


URL_MAPPING_LIST = [
    url(r'/api/authorize/user_auth/', UserAuthHandler, name='authorize_user_auth'),
    url(r'/api/authorize/token/auth/', AuthTokenHandler, name='authorize_auth_token'),
    url(r'/api/authorize/token/refresh/', RefreshTokenHandler, name='authorize_refresh_token'),
]
