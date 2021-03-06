# -*- coding: utf-8 -*-
# @File    : views.py
# @AUTH    : model

import bson
import json
import logging
from tornado.web import url
from web import BaseHandler, BaseAuthedHanlder, SuccessData, render, undefined
from commons.Helpers.Helper_pagenate import Page
from .utils.User import User, user_schema
from .utils.UserAuth import UserAuth, user_auth_schema

logger = logging.getLogger("main.system.views")


class UserHandler(BaseAuthedHanlder):
    async def add_tokens(self, params):
        return params

    @render
    async def get(self, user_id=None):
        if user_id:
            finds = await self.add_tokens({"id": user_id})
            user = await User.find(finds)
            return SuccessData(data=await user.to_front())
        else:
            use_pager = int(self.get_argument("use_pager", 1))
            page = int(self.get_argument("page", 1))
            items_per_page = int(self.get_argument("items_per_page", 20))
            search = self.arguments.get('search', "")
            orderby = self.arguments.get("orderby", "")

            searches = await self.add_tokens(user_schema.load(self.arguments, partial=True).data)
            if search:
                searches.update({"search": search})

            keys = []
            for _order in orderby.split(";"):
                if _order:
                    keys.append(_order)

            item_count = await User.count(searches)
            if use_pager:
                limit = items_per_page
                skip = (page - 1) * items_per_page
            else:
                limit = 0
                skip = 0
            user_cursor = User.search(searches, limit=limit, skip=skip).order_by(keys)
            data = [await user.to_front() async for user in user_cursor]
            pager = Page(data, use_pager=use_pager, page=page, items_per_page=items_per_page, item_count=item_count)
            return SuccessData(data=pager.items, info=pager.info)

    @render
    async def post(self, user_id=None):
        if user_id:
            finds = await self.add_tokens({"id": user_id})
            copys = user_schema.load(self.arguments, partial=True).data
            user = await User.find_and_copy(finds, copys)
            return SuccessData(id=user.id)
        else:
            creates = await self.add_tokens(user_schema.load(self.arguments).data)
            user = await User.create(creates)
            return SuccessData(id=user.id)

    @render
    async def put(self, user_id=None):
        finds = await self.add_tokens({"id": user_id})
        updates = user_schema.load(self.arguments, partial=True).data
        user = await User.find_and_update(finds, updates)
        return SuccessData(id=user.id)

    @render
    async def delete(self, user_id=None):
        finds = await self.add_tokens({"id": user_id})
        count = await User.find_and_delete(finds)
        return SuccessData(count=count)

    @render
    async def patch(self, user_id=None):
        create_list = []
        for __create in self.arguments.get("create", []):
            creates = await self.add_tokens(user_schema.load(__create).data)
            user = await User.create(creates)
            create_list.append(user.id)

        update_list = []
        for __update in self.arguments.get("update", []):
            if "find" in __update:
                finds = await self.add_tokens(__update.pop("find", {}))
                updates = user_schema.load(__update, partial=True).data
                user = await User.find_and_update(finds, updates)
                update_list.append(user.id)
            elif "search" in __update:
                searches = await self.add_tokens(__update.pop("search", {}))
                updates = user_schema.load(__update, partial=True).data
                user_list = await User.search_and_update(searches, updates)
                update_list.append(user_list)

        delete_list = []
        for __delete in self.arguments.get("delete", []):
            if "find" in __delete:
                finds = await self.add_tokens(__delete.pop("find", {}))
                count = await User.find_and_delete(finds)
                delete_list.append(count)
            elif "search" in __delete:
                searches = await self.add_tokens(__delete.pop("search", {}))
                count = await User.search_and_delete(searches)
                delete_list.append(count)

        return SuccessData(
            create_list=create_list,
            update_list=update_list,
            delete_list=delete_list,
        )

    def set_default_headers(self):
        self._headers.add("version", "1")


class UserAuthHandler(BaseAuthedHanlder):
    async def add_tokens(self, params):
        params['user_id'] = bson.ObjectId(self.tokens.get("user_id"))
        return params

    @render
    async def get(self, user_auth_id=None):
        if user_auth_id:
            finds = await self.add_tokens({"id": user_auth_id})
            user_auth = await UserAuth.find(finds)
            return SuccessData(data=await user_auth.to_front())
        else:
            use_pager = int(self.get_argument("use_pager", 1))
            page = int(self.get_argument("page", 1))
            items_per_page = int(self.get_argument("items_per_page", 20))
            search = self.arguments.get('search', "")
            orderby = self.arguments.get("orderby", "")

            searches = await self.add_tokens(user_auth_schema.load(self.arguments, partial=True).data)
            if search:
                searches.update({"search": search})

            keys = []
            for _order in orderby.split(";"):
                if _order:
                    keys.append(_order)

            item_count = await UserAuth.count(searches)
            if use_pager:
                limit = items_per_page
                skip = (page - 1) * items_per_page
            else:
                limit = 0
                skip = 0
            user_auth_cursor = UserAuth.search(searches, limit=limit, skip=skip).order_by(keys)
            data = [await user_auth.to_front() async for user_auth in user_auth_cursor]
            pager = Page(data, use_pager=use_pager, page=page, items_per_page=items_per_page, item_count=item_count)
            return SuccessData(data=pager.items, info=pager.info)

    @render
    async def post(self, user_auth_id=None):
        if user_auth_id:
            finds = await self.add_tokens({"id": user_auth_id})
            copys = user_auth_schema.load(self.arguments, partial=True).data
            user_auth = await UserAuth.find_and_copy(finds, copys)
            return SuccessData(id=user_auth.id)
        else:
            creates = await self.add_tokens(user_auth_schema.load(self.arguments).data)
            user_auth = await UserAuth.create(creates)
            return SuccessData(id=user_auth.id)

    @render
    async def put(self, user_auth_id=None):
        finds = await self.add_tokens({"id": user_auth_id})
        updates = user_auth_schema.load(self.arguments, partial=True).data
        user_auth = await UserAuth.find_and_update(finds, updates)
        return SuccessData(id=user_auth.id)

    @render
    async def delete(self, user_auth_id=None):
        finds = await self.add_tokens({"id": user_auth_id})
        count = await UserAuth.find_and_delete(finds)
        return SuccessData(count=count)

    @render
    async def patch(self, user_auth_id=None):
        create_list = []
        for __create in self.arguments.get("create", []):
            creates = await self.add_tokens(user_auth_schema.load(__create).data)
            user_auth = await UserAuth.create(creates)
            create_list.append(user_auth.id)

        update_list = []
        for __update in self.arguments.get("update", []):
            if "find" in __update:
                finds = await self.add_tokens(__update.pop("find", {}))
                updates = user_auth_schema.load(__update, partial=True).data
                user_auth = await UserAuth.find_and_update(finds, updates)
                update_list.append(user_auth.id)
            elif "search" in __update:
                searches = await self.add_tokens(__update.pop("search", {}))
                updates = user_auth_schema.load(__update, partial=True).data
                user_auth_list = await UserAuth.search_and_update(searches, updates)
                update_list.append(user_auth_list)

        delete_list = []
        for __delete in self.arguments.get("delete", []):
            if "find" in __delete:
                finds = await self.add_tokens(__delete.pop("find", {}))
                count = await UserAuth.find_and_delete(finds)
                delete_list.append(count)
            elif "search" in __delete:
                searches = await self.add_tokens(__delete.pop("search", {}))
                count = await UserAuth.search_and_delete(searches)
                delete_list.append(count)

        return SuccessData(
            create_list=create_list,
            update_list=update_list,
            delete_list=delete_list,
        )

    def set_default_headers(self):
        self._headers.add("version", "1")


URL_MAPPING_LIST = [
    url(r"/api/system/user/(?:([a-zA-Z0-9&%\.~-]+)/)?", UserHandler),
    url(r"/api/system/user_auth/(?:([a-zA-Z0-9&%\.~-]+)/)?", UserAuthHandler),
]
