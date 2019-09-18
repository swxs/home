# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.ValueGroup import ValueGroup

log = getLogger("views/ValueGroup")


class ValueGroupHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, value_group_id=None):
        if value_group_id:
            value_group = await ValueGroup.select(id=value_group_id)
            return SuccessData(
                await value_group.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            value_group_cursor = ValueGroup.search(**search_params)
            data = []
            async for value_group in value_group_cursor:
                data.append(await value_group.to_front())
            return SuccessData(data)
            # pager = Page(value_group_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, value_group_id=None):
        if value_group_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['value'] = self.get_argument('value', undefined)
            params['expression'] = self.get_argument('expression', undefined)
            value_group = await ValueGroup.select(id=value_group_id)
            value_group = await value_group.copy(**params)
            return SuccessData(
                value_group.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['value'] = self.get_argument('value', None)
            params['expression'] = self.get_argument('expression', None)
            value_group = await ValueGroup.create(**params)
            return SuccessData(
                value_group.id
            )

    @BaseHandler.ajax_base()
    async def put(self, value_group_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['value'] = self.get_argument('value', None)
        params['expression'] = self.get_argument('expression', None)
        value_group = await ValueGroup.select(id=value_group_id)
        value_group = await value_group.update(**params)
        return SuccessData(
            value_group.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, value_group_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['value'] = self.get_argument('value', undefined)
        params['expression'] = self.get_argument('expression', undefined)
        value_group = await ValueGroup.select(id=value_group_id)
        value_group = await value_group.update(**params)
        return SuccessData(
            value_group.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, value_group_id=None):
        value_group = await ValueGroup.select(id=value_group_id)
        await value_group.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
