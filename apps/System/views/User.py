# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model

import json
from tornado.web import url
from web.web import BaseHandler
from web.consts import undefined
from web.result import SuccessData
from web.decorator.render import render
from common.Helpers.Helper_pagenate import Page
from common.Utils.log_utils import getLogger
from ..utils.User import User, user_schema

log = getLogger("views/user")


class UserHandler(BaseHandler):
    @render
    async def get(self, user_id=None):
        if user_id:
            user = await User.select(id=user_id)
            return SuccessData(
                data=await user.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            order_by = self.get_argument("order_by", "")
            use_pager = int(self.get_argument("use_pager", 1))
            page = int(self.get_argument("page", 1))
            items_per_page = int(self.get_argument("items_per_page", 20))

            item_count = await User.count(**search_params)
            if use_pager:
                search_params.update({
                    "limit": items_per_page,
                    "skip": (page - 1) * items_per_page
                })
            order_by = [o for o in order_by.split(";") if bool(o)]
            user_cursor = User.search(**search_params).order_by(order_by)
            data = [await  user.to_front() async for user in user_cursor]
            pager = Page(data, use_pager=use_pager, page=page, items_per_page=items_per_page, item_count=item_count)
            return SuccessData(
                data=pager.items, 
                info=pager.info
            )


    @render
    async def post(self, user_id=None):
        if user_id:
            params = user_schema.load(self.arguments, partial=True)
            old_user = await User.select(id=user_id)
            new_user = await user.copy(**params.data)
            return SuccessData(
                id=new_user.id
            )
        else:
            params = user_schema.load(self.arguments)
            user = await User.create(**params.data)
            return SuccessData(
                id=user.id
            )

    @render
    async def put(self, user_id=None):
        params = user_schema.load(self.arguments)
        user = await User.find_and_update(id=user_id, **params.data)
        return SuccessData(
            id=user.id
        )

    @render
    async def patch(self, user_id=None):
        params = user_schema.load(self.arguments, partial=True)
        user = await User.find_and_update(id=user_id, **params.data)
        return SuccessData(
            id=user.id
        )

    @render
    async def delete(self, user_id=None):
        count = await User.find_and_delete(id=user_id)
        return SuccessData(
            count=count
        )

    def set_default_headers(self):
        self._headers.add("version", "1")


URL_MAPPING_LIST = [
    url(r"/api/system/user/(?:([a-zA-Z0-9&%\.~-]+)/)?", UserHandler),
]
