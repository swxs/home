# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.ContainerGroupSwitch import ContainerGroupSwitch
from common.Utils.log_utils import getLogger

log = getLogger("views/ContainerGroupSwitch")


class ContainerGroupSwitchHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_group_switch_id=None):
        if container_group_switch_id:
            container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
            return ContainerGroupSwitch.to_front()
        else:
            container_group_switch_list = ContainerGroupSwitch.filter()
            return [container_group_switch.to_front() for container_group_switch in container_group_switch_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        container_group_switch = ContainerGroupSwitch.create(params)
        return container_group_switch.to_front()

    @BaseHandler.ajax_base()
    def put(self, container_group_switch_id):
        params = self.get_all_arguments()
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch = container_group_switch.update(params)
        return container_group_switch.to_front()

    @BaseHandler.ajax_base()
    def patch(self, container_group_switch_id):
        params = self.get_all_arguments()
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch = container_group_switch.update(params)
        return container_group_switch.to_front()

    @BaseHandler.ajax_base()
    def delete(self, container_group_switch_id):
        container_group_switch = ContainerGroupSwitch.select(id=container_group_switch_id)
        container_group_switch.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
