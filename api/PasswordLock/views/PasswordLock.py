# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.PasswordLock import PasswordLock
from common.Utils.log_utils import getLogger

log = getLogger("views/PasswordLock")


class PasswordLockHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, password_lock_id=None):
        if password_lock_id:
            password_lock = PasswordLock.select(id=password_lock_id)
            return PasswordLock.to_front()
        else:
            password_lock_list = PasswordLock.filter()
            return [password_lock.to_front() for password_lock in password_lock_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        password_lock = PasswordLock.create(params)
        return password_lock.to_front()

    @BaseHandler.ajax_base()
    def put(self, password_lock_id):
        params = self.get_all_arguments()
        password_lock = PasswordLock.select(id=password_lock_id)
        password_lock = password_lock.update(params)
        return password_lock.to_front()

    @BaseHandler.ajax_base()
    def patch(self, password_lock_id):
        params = self.get_all_arguments()
        password_lock = PasswordLock.select(id=password_lock_id)
        password_lock = password_lock.update(params)
        return password_lock.to_front()

    @BaseHandler.ajax_base()
    def delete(self, password_lock_id):
        password_lock = PasswordLock.select(id=password_lock_id)
        password_lock.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
