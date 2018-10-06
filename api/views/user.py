# -*- coding: utf-8 -*-
# @File    : user.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:56

from base import BaseHandler
from api.consts.const import undefined
from api.utils.user import User


class UserHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def head(self, *args, **kwargs):
        return {"fields": User.__fields__, "methods": ["head", "get", "post", "put", "patch", "delete"]}


    @BaseHandler.ajax_base()
    def get(self, user_id=None):
        if user_id:
            user = User.select(id=user_id)
            return user.to_front()
        else:
            user_list = User.filter()
            return [user.to_front() for user in user_list]
            #  TODO: 添加参数, 允许以不特定参数查找指定的数据
            #  TODO: 支持分页
            #  TODO: 支持按请求排序
            # page = self.get_argument('page', 1)
            # paged_user_list = Page(
            #     user_list,
            #     page=page,
            #     items_per_page=USER_LIST_PER_PAGE
            # )
            # return [user.to_front() for user in paged_user_list]

    @BaseHandler.ajax_base()
    def post(self):
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = User.create(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base()
    def put(self, user_id):
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = User.select(id=user_id)
        user = user.update(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base()
    def patch(self, user_id):
        username = self.get_argument('username', undefined)
        nickname = self.get_argument('nickname', undefined)
        password = self.get_argument('password', undefined)
        userinfo_id = self.get_argument('userinfo_id', undefined)
        user = User.select(id=user_id)
        user = user.update(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base()
    def delete(self, user_id):
        user = User.select(id=user_id)
        user.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
