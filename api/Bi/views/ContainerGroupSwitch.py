# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.ContainerGroupSwitch import ContainerGroupSwitch

log = getLogger("views/ContainerGroupSwitch")


class ContainerGroupSwitchHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_group_switch_id=None):
        if container_group_switch_id:
            container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
            return SuccessData(
                container_group_switch.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            container_group_switch_list = ContainerGroupSwitch.search(**search_params).order_by()
            pager = Page(container_group_switch_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, container_group_switch_id=None):
        if container_group_switch_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            params['container_id_list'] = self.get_arguments('container_id_list', undefined)
            params['switch_list'] = self.get_arguments('switch_list', undefined)
            container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
            container_group_switch = container_group_switch.copy(**params)
            return SuccessData(
                container_group_switch.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            params['container_id_list'] = self.get_arguments('container_id_list', [])
            params['switch_list'] = self.get_arguments('switch_list', [])
            container_group_switch = ContainerGroupSwitch.create(**params)
            return SuccessData(
                container_group_switch.id
            )

    @BaseHandler.ajax_base()
    def put(self, container_group_switch_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['container_id_list'] = self.get_arguments('container_id_list', [])
        params['switch_list'] = self.get_arguments('switch_list', [])
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch = container_group_switch.update(**params)
        return SuccessData(
            container_group_switch.id
        )

    @BaseHandler.ajax_base()
    def patch(self, container_group_switch_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['container_id_list'] = self.get_arguments('container_id_list', undefined)
        params['switch_list'] = self.get_arguments('switch_list', undefined)
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch = container_group_switch.update(**params)
        return SuccessData(
            container_group_switch.id
        )

    @BaseHandler.ajax_base()
    def delete(self, container_group_switch_id=None):
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
