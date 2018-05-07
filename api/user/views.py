# -*- coding: utf-8 -*-
# @File    : views.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:56

from const import undefined, USER_LIST_PER_PAGE
from common.Utils.pagenate import Page
from base import BaseHandler
from utils import User


class UserHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, user_id=None):
        if user_id:
            user = User.select(id=user_id)
            return user.to_front()
        else:
            # page = self.get_argument('page', 1)
            #  TODO: 添加参数
            user_list = User.select()
            return [user.to_front() for user in user_list]
            # paged_user_list = Page(
            #     user_list,
            #     page=page,
            #     items_per_page=USER_LIST_PER_PAGE
            # )
            # return [user.to_front() for user in paged_user_list]

    @BaseHandler.ajax_base
    def post(self):
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = User.create(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base
    def put(self, user_id):
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = User.select(id=user_id)
        user = user.update(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base
    def patch(self, user_id):
        username = self.get_argument('username', undefined)
        nickname = self.get_argument('nickname', undefined)
        password = self.get_argument('password', undefined)
        userinfo_id = self.get_argument('userinfo_id', undefined)
        user = User.select(id=user_id)
        user = user.update(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base
    def delete(self, user_id):
        user = User.select(id=user_id)
        user.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
