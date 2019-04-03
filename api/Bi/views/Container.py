# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Container import Container
from common.Utils.log_utils import getLogger

log = getLogger("views/Container")


class ContainerHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_id=None):
        if container_id:
            container = Container.select(id=container_id)
            return Container.to_front()
        else:
            container_list = Container.filter()
            return [container.to_front() for container in container_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        container = Container.create(params)
        return container.to_front()

    @BaseHandler.ajax_base()
    def put(self, container_id):
        params = self.get_all_arguments()
        container = Container.select(id=container_id)
        container = container.update(params)
        return container.to_front()

    @BaseHandler.ajax_base()
    def patch(self, container_id):
        params = self.get_all_arguments()
        container = Container.select(id=container_id)
        container = container.update(params)
        return container.to_front()

    @BaseHandler.ajax_base()
    def delete(self, container_id):
        container = Container.select(id=container_id)
        container.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
