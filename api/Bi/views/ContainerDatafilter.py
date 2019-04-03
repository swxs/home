# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.ContainerDatafilter import ContainerDatafilter
from common.Utils.log_utils import getLogger

log = getLogger("views/ContainerDatafilter")


class ContainerDatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_datafilter_id=None):
        if container_datafilter_id:
            container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
            return ContainerDatafilter.to_front()
        else:
            container_datafilter_list = ContainerDatafilter.filter()
            return [container_datafilter.to_front() for container_datafilter in container_datafilter_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        container_datafilter = ContainerDatafilter.create(params)
        return container_datafilter.to_front()

    @BaseHandler.ajax_base()
    def put(self, container_datafilter_id):
        params = self.get_all_arguments()
        container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
        container_datafilter = container_datafilter.update(params)
        return container_datafilter.to_front()

    @BaseHandler.ajax_base()
    def patch(self, container_datafilter_id):
        params = self.get_all_arguments()
        container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
        container_datafilter = container_datafilter.update(params)
        return container_datafilter.to_front()

    @BaseHandler.ajax_base()
    def delete(self, container_datafilter_id):
        container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
        container_datafilter.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
