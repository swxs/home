# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.User import User

log = getLogger("views/User")


class UserHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, user_id=None):
        if user_id:
            user = User.select(id=user_id)
            return user.to_front()
        else:
            user_list = User.filter()
            return [user.to_front() for user in user_list]

    @BaseHandler.ajax_base()
    def post(self, user_id=None):
        if user_id:
            params = dict()
            params['username'] = self.get_argument('username', undefined)
            params['nickname'] = self.get_argument('nickname', undefined)
            params['password'] = self.get_argument('password', undefined)
            params['salt'] = self.get_argument('salt', undefined)
            params['avatar'] = self.get_argument('avatar', undefined)
            params['email'] = self.get_argument('email', undefined)
            params['mobile'] = self.get_argument('mobile', undefined)
            params['description'] = self.get_argument('description', undefined)
            user = User.select(id=user_id)
            user = user.copy(**params)
            return user.id
        else:
            params = dict()
            params['username'] = self.get_argument('username', None)
            params['nickname'] = self.get_argument('nickname', None)
            params['password'] = self.get_argument('password', None)
            params['salt'] = self.get_argument('salt', None)
            params['avatar'] = self.get_argument('avatar', None)
            params['email'] = self.get_argument('email', None)
            params['mobile'] = self.get_argument('mobile', None)
            params['description'] = self.get_argument('description', None)
            user = User.create(**params)
            return user.id

    @BaseHandler.ajax_base()
    def put(self, user_id=None):
        params = dict()
        params['username'] = self.get_argument('username', None)
        params['nickname'] = self.get_argument('nickname', None)
        params['password'] = self.get_argument('password', None)
        params['salt'] = self.get_argument('salt', None)
        params['avatar'] = self.get_argument('avatar', None)
        params['email'] = self.get_argument('email', None)
        params['mobile'] = self.get_argument('mobile', None)
        params['description'] = self.get_argument('description', None)
        user = User.select(id=user_id)
        user = user.update(**params)
        return user.id

    @BaseHandler.ajax_base()
    def patch(self, user_id=None):
        params = dict()
        params['username'] = self.get_argument('username', undefined)
        params['nickname'] = self.get_argument('nickname', undefined)
        params['password'] = self.get_argument('password', undefined)
        params['salt'] = self.get_argument('salt', undefined)
        params['avatar'] = self.get_argument('avatar', undefined)
        params['email'] = self.get_argument('email', undefined)
        params['mobile'] = self.get_argument('mobile', undefined)
        params['description'] = self.get_argument('description', undefined)
        user = User.select(id=user_id)
        user = user.update(**params)
        return user.id

    @BaseHandler.ajax_base()
    def delete(self, user_id=None):
        user = User.select(id=user_id)
        user.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
