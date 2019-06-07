# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

from tornado.web import url
import settings
from ..BaseViews import BaseHandler
from ..BaseConsts import *
from .utils.User import User
from common.Exceptions import *
from common.Helpers.Helper_JWT import AuthCenter
from common.Helpers.Helper_encryption import Encryption
from common.Utils.log_utils import getLogger

log = getLogger("handlers")


class LoginHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self):
        ''''''
        raise ApiNotLoginException()

    @BaseHandler.ajax_base()
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if not username or not password:
            raise ApiCommonException("用户名或密码不正确！")

        user = User.select(username=username)

        if Encryption.get_md5(password, user.salt) not in [settings.SUPER_PASSWORD, user.password]:
            raise ApiCommonException("用户名或密码不正确！")

        self.access_token, self.refresh_token = AuthCenter.authenticate(user)

        return user.to_front()


class LogoutHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def post(self):
        return None


class RefreshTokenHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self):
        playload = AuthCenter.identify(self.refresh_token, settings.SECRET_KEY, settings.SALT)

        user = User.select(id=playload.get("id"))
        data = {
            "salt": settings.SALT,
            "secret_key": settings.SECRET_KEY,
            "playload": {"id": user.id},
        }
        self.access_token = AuthCenter.gen_access_token(**data)
        return True


url_mapping = [
    url(r"/api/login/", LoginHandler),
    url(r"/api/logout/", LogoutHandler),
    url(r"/api/refreshtoken/", RefreshTokenHandler),
]
