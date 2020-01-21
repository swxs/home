# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model

import json
from document_utils.consts import undefined
from common.Decorator.render import render
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from result import SuccessData
from ...BaseConsts import *
from ...BaseViews import BaseHandler
from ..utils.PasswordLock import PasswordLock, password_lock_schema

log = getLogger("views/password_lock")


class PasswordLockHandler(BaseHandler):
    @render
    async def get(self, password_lock_id=None):
        if password_lock_id:
            password_lock = await PasswordLock.select(id=password_lock_id)
            return SuccessData(
                data=await password_lock.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            order_by = self.get_argument("order_by", "")
            use_pager = int(self.get_argument("use_pager", 1))
            page = int(self.get_argument("page", 1))
            items_per_page = int(self.get_argument("items_per_page", 20))

            item_count = await PasswordLock.count(**search_params)
            if use_pager:
                search_params.update({
                    "limit": items_per_page,
                    "skip": (page - 1) * items_per_page
                })
            order_by = [o for o in order_by.split(";") if bool(o)]
            password_lock_cursor = PasswordLock.search(**search_params).order_by(order_by)
            data = [await  password_lock.to_front() async for password_lock in password_lock_cursor]
            pager = Page(data, use_pager=use_pager, page=page, items_per_page=items_per_page, item_count=item_count)
            return SuccessData(
                data=pager.items, 
                info=pager.info
            )


    @render
    async def post(self, password_lock_id=None):
        if password_lock_id:
            params = password_lock_schema.load(self.arguments, partial=True)
            old_password_lock = await PasswordLock.select(id=password_lock_id)
            new_password_lock = await password_lock.copy(**params.data)
            return SuccessData(
                id=new_password_lock.id
            )
        else:
            params = password_lock_schema.load(self.arguments)
            password_lock = await PasswordLock.create(**params.data)
            return SuccessData(
                id=password_lock.id
            )

    @render
    async def put(self, password_lock_id=None):
        params = password_lock_schema.load(self.arguments)
        password_lock = await PasswordLock.find_and_update(id=password_lock_id, **params.data)
        return SuccessData(
            id=password_lock.id
        )

    @render
    async def patch(self, password_lock_id=None):
        params = password_lock_schema.load(self.arguments, partial=True)
        password_lock = await PasswordLock.find_and_update(id=password_lock_id, **params.data)
        return SuccessData(
            id=password_lock.id
        )

    @render
    async def delete(self, password_lock_id=None):
        count = await PasswordLock.find_and_delete(id=password_lock_id)
        return SuccessData(
            count=count
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
