# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.ContainerGroupDatafilter import ContainerGroupDatafilter

log = getLogger("views/ContainerGroupDatafilter")


class ContainerGroupDatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_group_datafilter_id=None):
        if container_group_datafilter_id:
            container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
            return SuccessData(
                container_group_datafilter.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            container_group_datafilter_list = ContainerGroupDatafilter.search(**search_params).order_by()
            pager = Page(container_group_datafilter_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, container_group_datafilter_id=None):
        if container_group_datafilter_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            params['container_id_list'] = self.get_arguments('container_id_list', undefined)
            container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
            container_group_datafilter = container_group_datafilter.copy(**params)
            return SuccessData(
                container_group_datafilter.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            params['container_id_list'] = self.get_arguments('container_id_list', [])
            container_group_datafilter = ContainerGroupDatafilter.create(**params)
            return SuccessData(
                container_group_datafilter.id
            )

    @BaseHandler.ajax_base()
    def put(self, container_group_datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['container_id_list'] = self.get_arguments('container_id_list', [])
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter = container_group_datafilter.update(**params)
        return SuccessData(
            container_group_datafilter.id
        )

    @BaseHandler.ajax_base()
    def patch(self, container_group_datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['container_id_list'] = self.get_arguments('container_id_list', undefined)
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter = container_group_datafilter.update(**params)
        return SuccessData(
            container_group_datafilter.id
        )

    @BaseHandler.ajax_base()
    def delete(self, container_group_datafilter_id=None):
        container_group_datafilter = ContainerGroupDatafilter.select(id=container_group_datafilter_id)
        container_group_datafilter.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
