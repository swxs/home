# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
from creater import Creater

class PasswordLockHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, password_lock_id=None):
        if password_lock_id:
            password_lock = Creater.get_password_lock_by_password_lock_id(password_lock_id)
            return password_lock.to_front()
        else:
            password_lock_list = Creater.get_password_lock_list()
            return password_lock_list.to_front()

    @BaseHandler.ajax_base
    def post(self):
        name = self.get_argument('name', None)
        key = self.get_argument('key', None)
        website = self.get_argument('website', None)
        user_id = self.get_argument('user_id', None)
        password_lock = Creater.create_password_lock(name=name, key=key, website=website, user_id=user_id)
        return password_lock.to_front()
    
    @BaseHandler.ajax_base
    def put(self, password_lock_id):
        name = self.get_argument('name', None)
        key = self.get_argument('key', None)
        website = self.get_argument('website', None)
        user_id = self.get_argument('user_id', None)
        password_lock = Creater.get_password_lock_by_password_lock_id(password_lock_id)
        password_lock.update_password_lock(name=name, key=key, website=website, user_id=user_id)
        return password_lock.to_front()

    @BaseHandler.ajax_base
    def patch(self, password_lock_id):
        name = self.get_argument('name', undefined)
        key = self.get_argument('key', undefined)
        website = self.get_argument('website', undefined)
        user_id = self.get_argument('user_id', undefined)
        password_lock = Creater.get_password_lock_by_password_lock_id(password_lock_id)
        password_lock.update_password_lock(name=name, key=key, website=website, user_id=user_id)
        return password_lock.to_front()

    @BaseHandler.ajax_base
    def delete(self, password_lock_id):
        password_lock = Creater.get_password_lock_by_password_lock_id(password_lock_id)
        password_lock.delete_password_lock()
        return None
