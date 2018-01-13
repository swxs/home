# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
from creater import Creater

class UserHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, user_id=None):
        ''''''
        if user_id:
            user = Creater.get_user_by_user_id(user_id)
            return user.to_front()
        else:
            user_list = Creater.get_user_list()
            return user_list.to_front()

    @BaseHandler.ajax_base
    def post(self):
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = Creater.create_user(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base
    def put(self, user_id):
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = Creater.get_user_by_user_id(user_id)
        user.update_user(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base
    def patch(self, user_id):
        username = self.get_argument('username', undefined)
        nickname = self.get_argument('nickname', undefined)
        password = self.get_argument('password', undefined)
        userinfo_id = self.get_argument('userinfo_id', undefined)
        user = Creater.get_user_by_user_id(user_id)
        user.update_user(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return user.to_front()

    @BaseHandler.ajax_base
    def delete(self, user_id):
        user = Creater.get_user_by_user_id(user_id)
        user.delete_user()
        return None
