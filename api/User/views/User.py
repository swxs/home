# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.User import User

log = getLogger("views/User")


class UserHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, user_id=None):
        if user_id:
            user = User.select(id=user_id)
            return SuccessData(
                user.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            user_list = User.search(**search_params).order_by()
            pager = Page(user_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, user_id=None):
        if user_id:
            params = dict()
            params['username'] = self.get_argument('username', undefined)
            params['nickname'] = self.get_argument('nickname', undefined)
            params['password'] = self.get_argument('password', undefined)
            params['salt'] = self.get_argument('salt', undefined)
            params['avatar'] = self.get_argument('avatar', undefined)
            params['email'] = self.get_argument('email', undefined)
            params['mobile'] = self.get_argument('mobile', undefined)
            params['description'] = self.get_argument('description', undefined)
            user = User.select(id=user_id)
            user = user.copy(**params)
            return SuccessData(
                user.id
            )
        else:
            params = dict()
            params['username'] = self.get_argument('username', None)
            params['nickname'] = self.get_argument('nickname', None)
            params['password'] = self.get_argument('password', None)
            params['salt'] = self.get_argument('salt', None)
            params['avatar'] = self.get_argument('avatar', None)
            params['email'] = self.get_argument('email', None)
            params['mobile'] = self.get_argument('mobile', None)
            params['description'] = self.get_argument('description', None)
            user = User.create(**params)
            return SuccessData(
                user.id
            )

    @BaseHandler.ajax_base()
    def put(self, user_id=None):
        params = dict()
        params['username'] = self.get_argument('username', None)
        params['nickname'] = self.get_argument('nickname', None)
        params['password'] = self.get_argument('password', None)
        params['salt'] = self.get_argument('salt', None)
        params['avatar'] = self.get_argument('avatar', None)
        params['email'] = self.get_argument('email', None)
        params['mobile'] = self.get_argument('mobile', None)
        params['description'] = self.get_argument('description', None)
        user = User.select(id=user_id)
        user = user.update(**params)
        return SuccessData(
            user.id
        )

    @BaseHandler.ajax_base()
    def patch(self, user_id=None):
        params = dict()
        params['username'] = self.get_argument('username', undefined)
        params['nickname'] = self.get_argument('nickname', undefined)
        params['password'] = self.get_argument('password', undefined)
        params['salt'] = self.get_argument('salt', undefined)
        params['avatar'] = self.get_argument('avatar', undefined)
        params['email'] = self.get_argument('email', undefined)
        params['mobile'] = self.get_argument('mobile', undefined)
        params['description'] = self.get_argument('description', undefined)
        user = User.select(id=user_id)
        user = user.update(**params)
        return SuccessData(
            user.id
        )

    @BaseHandler.ajax_base()
    def delete(self, user_id=None):
        user = User.select(id=user_id)
        user.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
