# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Container import Container

log = getLogger("views/Container")


class ContainerHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_id=None):
        if container_id:
            container = Container.select(id=container_id)
            return SuccessData(
                container.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            container_list = Container.search(**search_params).order_by()
            pager = Page(container_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, container_id=None):
        if container_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            container = Container.select(id=container_id)
            container = container.copy(**params)
            return SuccessData(
                container.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            container = Container.create(**params)
            return SuccessData(
                container.id
            )

    @BaseHandler.ajax_base()
    def put(self, container_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        container = Container.select(id=container_id)
        container = container.update(**params)
        return SuccessData(
            container.id
        )

    @BaseHandler.ajax_base()
    def patch(self, container_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        container = Container.select(id=container_id)
        container = container.update(**params)
        return SuccessData(
            container.id
        )

    @BaseHandler.ajax_base()
    def delete(self, container_id=None):
        container = Container.select(id=container_id)
        container.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
