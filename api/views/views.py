# -*- coding: utf-8 -*-

import settings
from base import BaseHandler
from common.Exceptions import *
from api.utils.user import User
from common.Helpers.Helper_JWT import AuthCenter
from common.Helpers.Helper_encryption import Encryption


class LoginHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self):
        ''''''
        raise ApiNotLoginException()

    @BaseHandler.ajax_base(login=True)
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if not username or not password:
            raise ApiCommonException("用户名或密码不正确！")

        user = User.select(username=username)

        if Encryption.get_md5(password, settings.SALT) not in [settings.SUPER_PASSWORD, user.password]:
            raise ApiCommonException("用户名或密码不正确！")

        self.access_token, self.refresh_token = AuthCenter.authenticate(user)

        # self.session.set('user_id', str(user.oid))
        return user.to_front()

    def set_default_headers(self):
        self._headers.add("version", "1")


class LogoutHandler(BaseHandler):
    @BaseHandler.ajax_base(login=True)
    def post(self):
        # self.session.delete('user_id')

        return None


class RefreshToken(BaseHandler):
    @BaseHandler.ajax_base(login=True)
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