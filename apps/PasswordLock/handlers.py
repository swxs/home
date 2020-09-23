# -*- coding: utf-8 -*-
# @File    : views.py
# @AUTH    : model

import bson
import json
from tornado.web import url
from web.web import BaseHandler, BaseAuthedHanlder
from web.consts import undefined
from web.result import SuccessData
from web.decorator.render import render
from common.Helpers.Helper_pagenate import Page
from common.Utils.log_utils import getLogger
from .utils.PasswordLock import PasswordLock, password_lock_schema

log = getLogger("views")


class PasswordLockHandler(BaseAuthedHanlder):
    async def add_tokens(self, params):
        params['user_id'] = bson.ObjectId(self.tokens.get("user_id"))
        return params

    @render
    async def get(self, password_lock_id=None):
        if password_lock_id:
            finds = await self.add_tokens({"id": password_lock_id})
            password_lock = await PasswordLock.find(finds)
            return SuccessData(data=await password_lock.to_front())
        else:
            use_pager = int(self.get_argument("use_pager", 1))
            page = int(self.get_argument("page", 1))
            items_per_page = int(self.get_argument("items_per_page", 20))
            search = self.arguments.get('search', "")
            orderby = self.arguments.get("orderby", "")

            searches = await self.add_tokens(password_lock_schema.load(self.arguments, partial=True).data)
            if search:
                searches.update({"search": search})

            keys = []
            for _order in orderby.split(";"):
                if _order:
                    keys.append(_order)

            item_count = await PasswordLock.count(searches)
            if use_pager:
                limit = items_per_page
                skip = (page - 1) * items_per_page
            else:
                limit = 0
                skip = 0
            password_lock_cursor = PasswordLock.search(searches, limit=limit, skip=skip).order_by(keys)
            data = [await password_lock.to_front() async for password_lock in password_lock_cursor]
            pager = Page(data, use_pager=use_pager, page=page, items_per_page=items_per_page, item_count=item_count)
            return SuccessData(data=pager.items, info=pager.info)

    @render
    async def post(self, password_lock_id=None):
        if password_lock_id:
            finds = await self.add_tokens({"id": password_lock_id})
            copys = password_lock_schema.load(self.arguments, partial=True).data
            password_lock = await PasswordLock.find_and_copy(finds, copys)
            return SuccessData(id=password_lock.id)
        else:
            creates = await self.add_tokens(password_lock_schema.load(self.arguments).data)
            password_lock = await PasswordLock.create(creates)
            return SuccessData(id=password_lock.id)

    @render
    async def put(self, password_lock_id=None):
        finds = await self.add_tokens({"id": password_lock_id})
        updates = password_lock_schema.load(self.arguments, partial=True).data
        password_lock = await PasswordLock.find_and_update(finds, updates)
        return SuccessData(id=password_lock.id)

    @render
    async def delete(self, password_lock_id=None):
        finds = await self.add_tokens({"id": password_lock_id})
        count = await PasswordLock.find_and_delete(finds)
        return SuccessData(count=count)

    @render
    async def patch(self, password_lock_id=None):
        create_list = []
        for __create in self.arguments.get("create", []):
            creates = await self.add_tokens(password_lock_schema.load(__create).data)
            password_lock = await PasswordLock.create(creates)
            create_list.append(password_lock.id)

        update_list = []
        for __update in self.arguments.get("update", []):
            if "find" in __update:
                finds = await self.add_tokens(__update.pop("find", {}))
                updates = password_lock_schema.load(__update, partial=True).data
                password_lock = await PasswordLock.find_and_update(finds, updates)
                update_list.append(password_lock.id)
            elif "search" in __update:
                searches = await self.add_tokens(__update.pop("search", {}))
                updates = password_lock_schema.load(__update, partial=True).data
                password_lock_list = await PasswordLock.search_and_update(searches, updates)
                update_list.append(password_lock_list)

        delete_list = []
        for __delete in self.arguments.get("delete", []):
            if "find" in __delete:
                finds = await self.add_tokens(__delete.pop("find", {}))
                count = await PasswordLock.find_and_delete(finds)
                delete_list.append(count)
            elif "search" in __delete:
                searches = await self.add_tokens(__delete.pop("search", {}))
                count = await PasswordLock.search_and_delete(searches)
                delete_list.append(count)

        return SuccessData(
            create_list=create_list,
            update_list=update_list,
            delete_list=delete_list,
        )

    def set_default_headers(self):
        self._headers.add("version", "1")


URL_MAPPING_LIST = [
    url(r"/api/password_lock/password_lock/(?:([a-zA-Z0-9&%\.~-]+)/)?", PasswordLockHandler),
]
