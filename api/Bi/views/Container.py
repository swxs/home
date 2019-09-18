# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Container import Container

log = getLogger("views/Container")


class ContainerHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, container_id=None):
        if container_id:
            container = await Container.select(id=container_id)
            return SuccessData(
                await container.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            container_cursor = Container.search(**search_params)
            data = []
            async for container in container_cursor:
                data.append(await container.to_front())
            return SuccessData(data)
            # pager = Page(container_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, container_id=None):
        if container_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            container = await Container.select(id=container_id)
            container = await container.copy(**params)
            return SuccessData(
                container.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            container = await Container.create(**params)
            return SuccessData(
                container.id
            )

    @BaseHandler.ajax_base()
    async def put(self, container_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        container = await Container.select(id=container_id)
        container = await container.update(**params)
        return SuccessData(
            container.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, container_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        container = await Container.select(id=container_id)
        container = await container.update(**params)
        return SuccessData(
            container.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, container_id=None):
        container = await Container.select(id=container_id)
        await container.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
