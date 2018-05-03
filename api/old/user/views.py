# -*- coding: utf-8 -*-

from const import undefined, USER_LIST_PER_PAGE
from common.Utils.pagenate import Page
from base import BaseHandler
import utils

class UserHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, user_id=None):
        if user_id:
            user = utils.get_user_by_user_id(user_id)
            return utils.to_front(user)
        else:
            page = self.get_argument('page', 1)
            user_list = utils.get_user_list()
            paged_user_list = Page(
                user_list,
                page=page,
                items_per_page=USER_LIST_PER_PAGE)
            return [utils.to_front(user) for user in paged_user_list]

    @BaseHandler.ajax_base
    def post(self):
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = utils.create_user(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return utils.to_front(user)
    
    @BaseHandler.ajax_base
    def put(self, user_id):
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = utils.get_user_by_user_id(user_id)
        utils.update_user(user, username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return utils.to_front(user)

    @BaseHandler.ajax_base
    def patch(self, user_id):
        username = self.get_argument('username', undefined)
        nickname = self.get_argument('nickname', undefined)
        password = self.get_argument('password', undefined)
        userinfo_id = self.get_argument('userinfo_id', undefined)
        user = utils.get_user_by_user_id(user_id)
        utils.update_user(user, username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return utils.to_front(user)

    @BaseHandler.ajax_base
    def delete(self, user_id):
        user = utils.get_user_by_user_id(user_id)
        utils.delete_user(user)
        return None
