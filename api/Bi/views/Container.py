# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Container import Container

log = getLogger("views/Container")


class ContainerHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_id=None):
        if container_id:
            container = Container.select(id=container_id)
            return container.to_front()
        else:
            container_list = Container.filter()
            return [container.to_front() for container in container_list]

    @BaseHandler.ajax_base()
    def post(self, container_id=None):
        if container_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            container = Container.select(id=container_id)
            container = container.copy(**params)
            return container.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            container = Container.create(**params)
            return container.id

    @BaseHandler.ajax_base()
    def put(self, container_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        container = Container.select(id=container_id)
        container = container.update(**params)
        return container.id

    @BaseHandler.ajax_base()
    def patch(self, container_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        container = Container.select(id=container_id)
        container = container.update(**params)
        return container.id

    @BaseHandler.ajax_base()
    def delete(self, container_id=None):
        container = Container.select(id=container_id)
        container.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
