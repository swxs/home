# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Publish import Publish

log = getLogger("views/Publish")


class PublishHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, publish_id=None):
        if publish_id:
            publish = await Publish.select(id=publish_id)
            return SuccessData(
                await publish.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            publish_cursor = Publish.search(**search_params)
            data = []
            async for publish in publish_cursor:
                data.append(await publish.to_front())
            return SuccessData(data)
            # pager = Page(publish_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, publish_id=None):
        if publish_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['region_id'] = self.get_argument('region_id', undefined)
            params['region_type_id'] = self.get_argument('region_type_id', undefined)
            params['user_id'] = self.get_argument('user_id', undefined)
            params['dashboard_id'] = self.get_argument('dashboard_id', undefined)
            params['ttype'] = self.get_argument('ttype', undefined)
            publish = await Publish.select(id=publish_id)
            publish = await publish.copy(**params)
            return SuccessData(
                publish.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['region_id'] = self.get_argument('region_id', None)
            params['region_type_id'] = self.get_argument('region_type_id', None)
            params['user_id'] = self.get_argument('user_id', None)
            params['dashboard_id'] = self.get_argument('dashboard_id', None)
            params['ttype'] = self.get_argument('ttype', None)
            publish = await Publish.create(**params)
            return SuccessData(
                publish.id
            )

    @BaseHandler.ajax_base()
    async def put(self, publish_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['region_id'] = self.get_argument('region_id', None)
        params['region_type_id'] = self.get_argument('region_type_id', None)
        params['user_id'] = self.get_argument('user_id', None)
        params['dashboard_id'] = self.get_argument('dashboard_id', None)
        params['ttype'] = self.get_argument('ttype', None)
        publish = await Publish.select(id=publish_id)
        publish = await publish.update(**params)
        return SuccessData(
            publish.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, publish_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['region_id'] = self.get_argument('region_id', undefined)
        params['region_type_id'] = self.get_argument('region_type_id', undefined)
        params['user_id'] = self.get_argument('user_id', undefined)
        params['dashboard_id'] = self.get_argument('dashboard_id', undefined)
        params['ttype'] = self.get_argument('ttype', undefined)
        publish = await Publish.select(id=publish_id)
        publish = await publish.update(**params)
        return SuccessData(
            publish.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, publish_id=None):
        publish = await Publish.select(id=publish_id)
        await publish.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
