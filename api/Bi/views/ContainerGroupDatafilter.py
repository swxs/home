# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.ContainerGroupDatafilter import ContainerGroupDatafilter

log = getLogger("views/ContainerGroupDatafilter")


class ContainerGroupDatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_group_datafilter_id=None):
        if container_group_datafilter_id:
            container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
            return container_group_datafilter.to_front()
        else:
            container_group_datafilter_list = ContainerGroupDatafilter.filter()
            return [container_group_datafilter.to_front() for container_group_datafilter in container_group_datafilter_list]

    @BaseHandler.ajax_base()
    def post(self, container_group_datafilter_id=None):
        if container_group_datafilter_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            params['container_id_list'] = self.get_arguments('container_id_list', undefined)
            container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
            container_group_datafilter = container_group_datafilter.copy(**params)
            return container_group_datafilter.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            params['container_id_list'] = self.get_arguments('container_id_list', [])
            container_group_datafilter = ContainerGroupDatafilter.create(**params)
            return container_group_datafilter.id

    @BaseHandler.ajax_base()
    def put(self, container_group_datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['container_id_list'] = self.get_arguments('container_id_list', [])
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter = container_group_datafilter.update(**params)
        return container_group_datafilter.id

    @BaseHandler.ajax_base()
    def patch(self, container_group_datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['container_id_list'] = self.get_arguments('container_id_list', undefined)
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter = container_group_datafilter.update(**params)
        return container_group_datafilter.id

    @BaseHandler.ajax_base()
    def delete(self, container_group_datafilter_id=None):
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
