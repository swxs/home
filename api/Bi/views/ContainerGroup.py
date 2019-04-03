# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.ContainerGroup import ContainerGroup
from common.Utils.log_utils import getLogger

log = getLogger("views/ContainerGroup")


class ContainerGroupHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_group_id=None):
        if container_group_id:
            container_group = ContainerGroup.select(id=container_group_id)
            return ContainerGroup.to_front()
        else:
            container_group_list = ContainerGroup.filter()
            return [container_group.to_front() for container_group in container_group_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        container_group = ContainerGroup.create(params)
        return container_group.to_front()

    @BaseHandler.ajax_base()
    def put(self, container_group_id):
        params = self.get_all_arguments()
        container_group = ContainerGroup.select(id=container_group_id)
        container_group = container_group.update(params)
        return container_group.to_front()

    @BaseHandler.ajax_base()
    def patch(self, container_group_id):
        params = self.get_all_arguments()
        container_group = ContainerGroup.select(id=container_group_id)
        container_group = container_group.update(params)
        return container_group.to_front()

    @BaseHandler.ajax_base()
    def delete(self, container_group_id):
        container_group = ContainerGroup.select(id=container_group_id)
        container_group.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
