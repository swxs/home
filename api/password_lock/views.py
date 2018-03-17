# -*- coding: utf-8 -*-

from const import undefined, PASSWORDLOCK_LIST_PER_PAGE
from common.Utils.pagenate import Page
from base import BaseHandler
import utils

class PasswordLockHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, password_lock_id=None):
        if password_lock_id:
            password_lock = utils.get_password_lock_by_password_lock_id(password_lock_id)
            return utils.to_front(password_lock)
        else:
            page = self.get_argument('page', 1)
            password_lock_list = utils.get_password_lock_list()
            paged_password_lock_list = Page(
                password_lock_list,
                page=page,
                items_per_page=PASSWORDLOCK_LIST_PER_PAGE)
            return [utils.to_front(password_lock) for password_lock in paged_password_lock_list]

    @BaseHandler.ajax_base
    def post(self):
        name = self.get_argument('name', None)
        key = self.get_argument('key', None)
        website = self.get_argument('website', None)
        user_id = self.get_argument('user_id', None)
        password_lock = utils.create_password_lock(name=name, key=key, website=website, user_id=user_id)
        return utils.to_front(password_lock)
    
    @BaseHandler.ajax_base
    def put(self, password_lock_id):
        name = self.get_argument('name', None)
        key = self.get_argument('key', None)
        website = self.get_argument('website', None)
        user_id = self.get_argument('user_id', None)
        password_lock = utils.get_password_lock_by_password_lock_id(password_lock_id)
        utils.update_password_lock(password_lock, name=name, key=key, website=website, user_id=user_id)
        return utils.to_front(password_lock)

    @BaseHandler.ajax_base
    def patch(self, password_lock_id):
        name = self.get_argument('name', undefined)
        key = self.get_argument('key', undefined)
        website = self.get_argument('website', undefined)
        user_id = self.get_argument('user_id', undefined)
        password_lock = utils.get_password_lock_by_password_lock_id(password_lock_id)
        utils.update_password_lock(password_lock, name=name, key=key, website=website, user_id=user_id)
        return utils.to_front(password_lock)

    @BaseHandler.ajax_base
    def delete(self, password_lock_id):
        password_lock = utils.get_password_lock_by_password_lock_id(password_lock_id)
        utils.delete_password_lock(password_lock)
        return None
