# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.ContainerDatafilter import ContainerDatafilter

log = getLogger("views/ContainerDatafilter")


class ContainerDatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, container_datafilter_id=None):
        if container_datafilter_id:
            container_datafilter = await ContainerDatafilter.select(id=container_datafilter_id)
            return SuccessData(
                await container_datafilter.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            container_datafilter_cursor = ContainerDatafilter.search(**search_params)
            data = []
            async for container_datafilter in container_datafilter_cursor:
                data.append(await container_datafilter.to_front())
            return SuccessData(data)
            # pager = Page(container_datafilter_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, container_datafilter_id=None):
        if container_datafilter_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            params['data_filter_id'] = self.get_argument('data_filter_id', undefined)
            container_datafilter = await ContainerDatafilter.select(id=container_datafilter_id)
            container_datafilter = await container_datafilter.copy(**params)
            return SuccessData(
                container_datafilter.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            params['data_filter_id'] = self.get_argument('data_filter_id', None)
            container_datafilter = await ContainerDatafilter.create(**params)
            return SuccessData(
                container_datafilter.id
            )

    @BaseHandler.ajax_base()
    async def put(self, container_datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['data_filter_id'] = self.get_argument('data_filter_id', None)
        container_datafilter = await ContainerDatafilter.select(id=container_datafilter_id)
        container_datafilter = await container_datafilter.update(**params)
        return SuccessData(
            container_datafilter.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, container_datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['data_filter_id'] = self.get_argument('data_filter_id', undefined)
        container_datafilter = await ContainerDatafilter.select(id=container_datafilter_id)
        container_datafilter = await container_datafilter.update(**params)
        return SuccessData(
            container_datafilter.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, container_datafilter_id=None):
        container_datafilter = await ContainerDatafilter.select(id=container_datafilter_id)
        await container_datafilter.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
