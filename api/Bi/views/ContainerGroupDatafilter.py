# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.ContainerGroupDatafilter import ContainerGroupDatafilter
from common.Utils.log_utils import getLogger

log = getLogger("views/ContainerGroupDatafilter")


class ContainerGroupDatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_group_datafilter_id=None):
        if container_group_datafilter_id:
            container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
            return ContainerGroupDatafilter.to_front()
        else:
            container_group_datafilter_list = ContainerGroupDatafilter.filter()
            return [container_group_datafilter.to_front() for container_group_datafilter in container_group_datafilter_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        container_group_datafilter = ContainerGroupDatafilter.create(params)
        return container_group_datafilter.to_front()

    @BaseHandler.ajax_base()
    def put(self, container_group_datafilter_id):
        params = self.get_all_arguments()
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter = container_group_datafilter.update(params)
        return container_group_datafilter.to_front()

    @BaseHandler.ajax_base()
    def patch(self, container_group_datafilter_id):
        params = self.get_all_arguments()
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter = container_group_datafilter.update(params)
        return container_group_datafilter.to_front()

    @BaseHandler.ajax_base()
    def delete(self, container_group_datafilter_id):
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
