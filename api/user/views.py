# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
import enums as enums
import utils as utils

class UserHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, user_id=None):
        ''''''
        if user_id:
            user = utils.get_user_by_user_id(user_id)
            return utils.to_front(user)
        else:
            user_list = utils.get_user_list()
            return [utils.to_front(user) for user in user_list]


    @BaseHandler.ajax_base
    def post(self):
        
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = utils.create(username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return utils.to_front(user)
    
    @BaseHandler.ajax_base
    def put(self, user_id):
        
        username = self.get_argument('username', None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        userinfo_id = self.get_argument('userinfo_id', None)
        user = utils.get_user_by_user_id(user_id)
        user = utils.update(user, username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return utils.to_front(user)
    
    @BaseHandler.ajax_base
    def patch(self, user_id):
        
        username = self.get_argument('username', undefined)
        nickname = self.get_argument('nickname', undefined)
        password = self.get_argument('password', undefined)
        userinfo_id = self.get_argument('userinfo_id', undefined)
        user = utils.get_user_by_user_id(user_id)
        user = utils.update(user, username=username, nickname=nickname, password=password, userinfo_id=userinfo_id)
        return utils.to_front(user)
            
    @BaseHandler.ajax_base
    def delete(self, user_id):
        user = utils.get_user_by_user_id(user_id)
        utils.delete(user)
        return None
