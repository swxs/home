# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
from api.password_lock.creater import Creater


class UserPasswordLockHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, password_lock_id=None):
        if password_lock_id:
            user_id = self.current_user.oid
            password_lock = Creater.get_password_lock_by_password_lock_id_user_id(password_lock_id, user_id)
            return password_lock.to_front()
        else:
            user_id = self.current_user.oid
            password_lock_list = Creater.get_password_lock_list_by_user_id(user_id)
            return password_lock_list.to_front()

    @BaseHandler.ajax_base
    def post(self):
        user_id = self.current_user.oid
        name = self.get_argument('name', None)
        website = self.get_argument('website', None)
        password_lock = Creater.create_password_lock(name=name, website=website, user_id=user_id)
        return password_lock.to_front()

    @BaseHandler.ajax_base
    def put(self, password_lock_id):
        user_id = self.current_user.oid
        name = self.get_argument('name', None)
        website = self.get_argument('website', None)
        password_lock = Creater.get_password_lock_by_password_lock_id_user_id(password_lock_id, user_id)
        password_lock.update_password_lock(name=name, website=website)
        return password_lock.to_front()

    @BaseHandler.ajax_base
    def patch(self, password_lock_id):
        user_id = self.current_user.oid
        name = self.get_argument('name', undefined)
        website = self.get_argument('website', undefined)
        password_lock = Creater.get_password_lock_by_password_lock_id_user_id(password_lock_id, user_id)
        password_lock.update_password_lock(name=name, website=website)
        return password_lock.to_front()

    @BaseHandler.ajax_base
    def delete(self, password_lock_id):
        user_id = self.current_user.oid
        password_lock = Creater.get_password_lock_by_password_lock_id_user_id(password_lock_id, user_id)
        password_lock.delete_password_lock()
        return None
