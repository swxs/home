# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.ContainerDatafilter import ContainerDatafilter

log = getLogger("views/ContainerDatafilter")


class ContainerDatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_datafilter_id=None):
        if container_datafilter_id:
            container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
            return container_datafilter.to_front()
        else:
            container_datafilter_list = ContainerDatafilter.filter()
            return [container_datafilter.to_front() for container_datafilter in container_datafilter_list]

    @BaseHandler.ajax_base()
    def post(self, container_datafilter_id=None):
        if container_datafilter_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            params['data_filter_id'] = self.get_argument('data_filter_id', undefined)
            container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
            container_datafilter = container_datafilter.copy(**params)
            return container_datafilter.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            params['data_filter_id'] = self.get_argument('data_filter_id', None)
            container_datafilter = ContainerDatafilter.create(**params)
            return container_datafilter.id

    @BaseHandler.ajax_base()
    def put(self, container_datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['data_filter_id'] = self.get_argument('data_filter_id', None)
        container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
        container_datafilter = container_datafilter.update(**params)
        return container_datafilter.id

    @BaseHandler.ajax_base()
    def patch(self, container_datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['data_filter_id'] = self.get_argument('data_filter_id', undefined)
        container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
        container_datafilter = container_datafilter.update(**params)
        return container_datafilter.id

    @BaseHandler.ajax_base()
    def delete(self, container_datafilter_id=None):
        container_datafilter = ContainerDatafilter.select(id=container_datafilter_id)
        container_datafilter.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
