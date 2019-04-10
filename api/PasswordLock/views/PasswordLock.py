# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.PasswordLock import PasswordLock

log = getLogger("views/PasswordLock")


class PasswordLockHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, password_lock_id=None):
        if password_lock_id:
            password_lock = PasswordLock.select(id=password_lock_id)
            return password_lock.to_front()
        else:
            password_lock_list = PasswordLock.filter()
            return [password_lock.to_front() for password_lock in password_lock_list]

    @BaseHandler.ajax_base()
    def post(self, password_lock_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['key'] = self.get_argument('key', None)
        params['website'] = self.get_argument('website', None)
        params['user_id'] = self.get_argument('user_id', None)
        password_lock = PasswordLock.create(**params)
        return password_lock.id

    @BaseHandler.ajax_base()
    def put(self, password_lock_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['key'] = self.get_argument('key', None)
        params['website'] = self.get_argument('website', None)
        params['user_id'] = self.get_argument('user_id', None)
        password_lock = PasswordLock.select(id=password_lock_id)
        password_lock = password_lock.update(**params)
        return password_lock.id

    @BaseHandler.ajax_base()
    def patch(self, password_lock_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['key'] = self.get_argument('key', undefined)
        params['website'] = self.get_argument('website', undefined)
        params['user_id'] = self.get_argument('user_id', undefined)
        password_lock = PasswordLock.select(id=password_lock_id)
        password_lock = password_lock.update(**params)
        return password_lock.id

    @BaseHandler.ajax_base()
    def delete(self, password_lock_id=None):
        password_lock = PasswordLock.select(id=password_lock_id)
        password_lock.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
