# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Datafilter import Datafilter

log = getLogger("views/Datafilter")


class DatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, datafilter_id=None):
        if datafilter_id:
            datafilter = await Datafilter.select(id=datafilter_id)
            return SuccessData(
                await datafilter.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            datafilter_cursor = Datafilter.search(**search_params)
            data = []
            async for datafilter in datafilter_cursor:
                data.append(await datafilter.to_front())
            return SuccessData(data)
            # pager = Page(datafilter_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, datafilter_id=None):
        if datafilter_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['column_id'] = self.get_argument('column_id', undefined)
            params['worktable_id'] = self.get_argument('worktable_id', undefined)
            params['dtype'] = self.get_argument('dtype', undefined)
            params['custom_attr'] = self.get_argument('custom_attr', undefined)
            datafilter = await Datafilter.select(id=datafilter_id)
            datafilter = await datafilter.copy(**params)
            return SuccessData(
                datafilter.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['column_id'] = self.get_argument('column_id', None)
            params['worktable_id'] = self.get_argument('worktable_id', None)
            params['dtype'] = self.get_argument('dtype', None)
            params['custom_attr'] = self.get_argument('custom_attr', None)
            datafilter = await Datafilter.create(**params)
            return SuccessData(
                datafilter.id
            )

    @BaseHandler.ajax_base()
    async def put(self, datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['column_id'] = self.get_argument('column_id', None)
        params['worktable_id'] = self.get_argument('worktable_id', None)
        params['dtype'] = self.get_argument('dtype', None)
        params['custom_attr'] = self.get_argument('custom_attr', None)
        datafilter = await Datafilter.select(id=datafilter_id)
        datafilter = await datafilter.update(**params)
        return SuccessData(
            datafilter.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['column_id'] = self.get_argument('column_id', undefined)
        params['worktable_id'] = self.get_argument('worktable_id', undefined)
        params['dtype'] = self.get_argument('dtype', undefined)
        params['custom_attr'] = self.get_argument('custom_attr', undefined)
        datafilter = await Datafilter.select(id=datafilter_id)
        datafilter = await datafilter.update(**params)
        return SuccessData(
            datafilter.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, datafilter_id=None):
        datafilter = await Datafilter.select(id=datafilter_id)
        await datafilter.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
