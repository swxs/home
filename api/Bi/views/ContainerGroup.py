# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.ContainerGroup import ContainerGroup

log = getLogger("views/ContainerGroup")


class ContainerGroupHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_group_id=None):
        if container_group_id:
            container_group = ContainerGroup.select(id=container_group_id)
            return container_group.to_front()
        else:
            container_group_list = ContainerGroup.filter()
            return [container_group.to_front() for container_group in container_group_list]

    @BaseHandler.ajax_base()
    def post(self, container_group_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['container_id_list'] = self.get_arguments('container_id_list', [])
        params['layout_list'] = self.get_arguments('layout_list', [])
        container_group = ContainerGroup.create(**params)
        return container_group.id

    @BaseHandler.ajax_base()
    def put(self, container_group_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['container_id_list'] = self.get_arguments('container_id_list', [])
        params['layout_list'] = self.get_arguments('layout_list', [])
        container_group = ContainerGroup.select(id=container_group_id)
        container_group = container_group.update(**params)
        return container_group.id

    @BaseHandler.ajax_base()
    def patch(self, container_group_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['container_id_list'] = self.get_arguments('container_id_list', undefined)
        params['layout_list'] = self.get_arguments('layout_list', undefined)
        container_group = ContainerGroup.select(id=container_group_id)
        container_group = container_group.update(**params)
        return container_group.id

    @BaseHandler.ajax_base()
    def delete(self, container_group_id=None):
        container_group = ContainerGroup.select(id=container_group_id)
        container_group.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
