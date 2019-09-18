# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Worktable import Worktable

log = getLogger("views/Worktable")


class WorktableHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, worktable_id=None):
        if worktable_id:
            worktable = await Worktable.select(id=worktable_id)
            return SuccessData(
                await worktable.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            worktable_cursor = Worktable.search(**search_params)
            data = []
            async for worktable in worktable_cursor:
                data.append(await worktable.to_front())
            return SuccessData(data)
            # pager = Page(worktable_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, worktable_id=None):
        if worktable_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['datasource_id'] = self.get_argument('datasource_id', undefined)
            params['engine'] = self.get_argument('engine', undefined)
            params['status'] = self.get_argument('status', undefined)
            params['description'] = self.get_argument('description', undefined)
            worktable = await Worktable.select(id=worktable_id)
            worktable = await worktable.copy(**params)
            return SuccessData(
                worktable.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['datasource_id'] = self.get_argument('datasource_id', None)
            params['engine'] = self.get_argument('engine', None)
            params['status'] = self.get_argument('status', None)
            params['description'] = self.get_argument('description', None)
            worktable = await Worktable.create(**params)
            return SuccessData(
                worktable.id
            )

    @BaseHandler.ajax_base()
    async def put(self, worktable_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['datasource_id'] = self.get_argument('datasource_id', None)
        params['engine'] = self.get_argument('engine', None)
        params['status'] = self.get_argument('status', None)
        params['description'] = self.get_argument('description', None)
        worktable = await Worktable.select(id=worktable_id)
        worktable = await worktable.update(**params)
        return SuccessData(
            worktable.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, worktable_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['datasource_id'] = self.get_argument('datasource_id', undefined)
        params['engine'] = self.get_argument('engine', undefined)
        params['status'] = self.get_argument('status', undefined)
        params['description'] = self.get_argument('description', undefined)
        worktable = await Worktable.select(id=worktable_id)
        worktable = await worktable.update(**params)
        return SuccessData(
            worktable.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, worktable_id=None):
        worktable = await Worktable.select(id=worktable_id)
        await worktable.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
