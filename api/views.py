# -*- coding: utf-8 -*-

import datetime
import re
import tornado

import settings
from base import BaseHandler
from api.user.creater import Creater as user_creater
from common.Exceptions.NotLoginException import NotLoginException
from common.Exceptions.ValidateException import ValidateException


class IndexHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self):
        return []

class LoginHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self):
        ''''''
        raise NotLoginException()

    @BaseHandler.ajax_base
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if not username or not password:
            raise ValidateException(u"用户名或密码")

        user = user_creater.get_user_by_username(username=username)

        if user.get_real_password(password) not in [settings.SUPER_PASSWORD, user.password]:
            raise ValidateException(u"用户名或密码")

        self.session.set('user_id', str(user.oid))
        return user.to_front()


class LogoutHandler(BaseHandler):
    @BaseHandler.ajax_base
    def post(self):
        self.session.delete('user_id')
        return None