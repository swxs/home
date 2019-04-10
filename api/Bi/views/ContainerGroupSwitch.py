# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.ContainerGroupSwitch import ContainerGroupSwitch

log = getLogger("views/ContainerGroupSwitch")


class ContainerGroupSwitchHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_group_switch_id=None):
        if container_group_switch_id:
            container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
            return container_group_switch.to_front()
        else:
            container_group_switch_list = ContainerGroupSwitch.filter()
            return [container_group_switch.to_front() for container_group_switch in container_group_switch_list]

    @BaseHandler.ajax_base()
    def post(self, container_group_switch_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['container_id_list'] = self.get_arguments('container_id_list', [])
        params['switch_list'] = self.get_arguments('switch_list', [])
        container_group_switch = ContainerGroupSwitch.create(**params)
        return container_group_switch.id

    @BaseHandler.ajax_base()
    def put(self, container_group_switch_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['container_id_list'] = self.get_arguments('container_id_list', [])
        params['switch_list'] = self.get_arguments('switch_list', [])
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch = container_group_switch.update(**params)
        return container_group_switch.id

    @BaseHandler.ajax_base()
    def patch(self, container_group_switch_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['container_id_list'] = self.get_arguments('container_id_list', undefined)
        params['switch_list'] = self.get_arguments('switch_list', undefined)
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch = container_group_switch.update(**params)
        return container_group_switch.id

    @BaseHandler.ajax_base()
    def delete(self, container_group_switch_id=None):
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
