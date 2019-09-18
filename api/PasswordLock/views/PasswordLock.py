# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.PasswordLock import PasswordLock

log = getLogger("views/PasswordLock")


class PasswordLockHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, password_lock_id=None):
        if password_lock_id:
            password_lock = await PasswordLock.select(id=password_lock_id)
            return SuccessData(
                await password_lock.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            password_lock_cursor = PasswordLock.search(**search_params)
            data = []
            async for password_lock in password_lock_cursor:
                data.append(await password_lock.to_front())
            return SuccessData(data)
            # pager = Page(password_lock_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, password_lock_id=None):
        if password_lock_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['key'] = self.get_argument('key', undefined)
            params['website'] = self.get_argument('website', undefined)
            params['user_id'] = self.get_argument('user_id', undefined)
            password_lock = await PasswordLock.select(id=password_lock_id)
            password_lock = await password_lock.copy(**params)
            return SuccessData(
                password_lock.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['key'] = self.get_argument('key', None)
            params['website'] = self.get_argument('website', None)
            params['user_id'] = self.get_argument('user_id', None)
            password_lock = await PasswordLock.create(**params)
            return SuccessData(
                password_lock.id
            )

    @BaseHandler.ajax_base()
    async def put(self, password_lock_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['key'] = self.get_argument('key', None)
        params['website'] = self.get_argument('website', None)
        params['user_id'] = self.get_argument('user_id', None)
        password_lock = await PasswordLock.select(id=password_lock_id)
        password_lock = await password_lock.update(**params)
        return SuccessData(
            password_lock.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, password_lock_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['key'] = self.get_argument('key', undefined)
        params['website'] = self.get_argument('website', undefined)
        params['user_id'] = self.get_argument('user_id', undefined)
        password_lock = await PasswordLock.select(id=password_lock_id)
        password_lock = await password_lock.update(**params)
        return SuccessData(
            password_lock.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, password_lock_id=None):
        password_lock = await PasswordLock.select(id=password_lock_id)
        await password_lock.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
