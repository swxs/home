# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.ContainerGroupSwitch import ContainerGroupSwitch

log = getLogger("views/ContainerGroupSwitch")


class ContainerGroupSwitchHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, container_group_switch_id=None):
        if container_group_switch_id:
            container_group_switch = await ContainerGroupSwitch.select(id=container_group_switch_id)
            return SuccessData(
                await container_group_switch.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            container_group_switch_cursor = ContainerGroupSwitch.search(**search_params)
            data = []
            async for container_group_switch in container_group_switch_cursor:
                data.append(await container_group_switch.to_front())
            return SuccessData(data)
            # pager = Page(container_group_switch_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, container_group_switch_id=None):
        if container_group_switch_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            params['container_id_list'] = self.get_arguments('container_id_list', undefined)
            params['switch_list'] = self.get_arguments('switch_list', undefined)
            container_group_switch = await ContainerGroupSwitch.select(id=container_group_switch_id)
            container_group_switch = await container_group_switch.copy(**params)
            return SuccessData(
                container_group_switch.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            params['container_id_list'] = self.get_arguments('container_id_list', [])
            params['switch_list'] = self.get_arguments('switch_list', [])
            container_group_switch = await ContainerGroupSwitch.create(**params)
            return SuccessData(
                container_group_switch.id
            )

    @BaseHandler.ajax_base()
    async def put(self, container_group_switch_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['container_id_list'] = self.get_arguments('container_id_list', [])
        params['switch_list'] = self.get_arguments('switch_list', [])
        container_group_switch = await ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch = await container_group_switch.update(**params)
        return SuccessData(
            container_group_switch.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, container_group_switch_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['container_id_list'] = self.get_arguments('container_id_list', undefined)
        params['switch_list'] = self.get_arguments('switch_list', undefined)
        container_group_switch = await ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch = await container_group_switch.update(**params)
        return SuccessData(
            container_group_switch.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, container_group_switch_id=None):
        container_group_switch = await ContainerGroupSwitch.select(id=container_group_switch_id)
        await container_group_switch.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
