# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Publish import Publish

log = getLogger("views/Publish")


class PublishHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, publish_id=None):
        if publish_id:
            publish = Publish.select(id=publish_id)
            return SuccessData(
                publish.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            publish_list = Publish.search(**search_params).order_by()
            pager = Page(publish_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, publish_id=None):
        if publish_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['region_id'] = self.get_argument('region_id', undefined)
            params['region_type_id'] = self.get_argument('region_type_id', undefined)
            params['user_id'] = self.get_argument('user_id', undefined)
            params['dashboard_id'] = self.get_argument('dashboard_id', undefined)
            params['ttype'] = self.get_argument('ttype', undefined)
            publish = Publish.select(id=publish_id)
            publish = publish.copy(**params)
            return SuccessData(
                publish.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['region_id'] = self.get_argument('region_id', None)
            params['region_type_id'] = self.get_argument('region_type_id', None)
            params['user_id'] = self.get_argument('user_id', None)
            params['dashboard_id'] = self.get_argument('dashboard_id', None)
            params['ttype'] = self.get_argument('ttype', None)
            publish = Publish.create(**params)
            return SuccessData(
                publish.id
            )

    @BaseHandler.ajax_base()
    def put(self, publish_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['region_id'] = self.get_argument('region_id', None)
        params['region_type_id'] = self.get_argument('region_type_id', None)
        params['user_id'] = self.get_argument('user_id', None)
        params['dashboard_id'] = self.get_argument('dashboard_id', None)
        params['ttype'] = self.get_argument('ttype', None)
        publish = Publish.select(id=publish_id)
        publish = publish.update(**params)
        return SuccessData(
            publish.id
        )

    @BaseHandler.ajax_base()
    def patch(self, publish_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['region_id'] = self.get_argument('region_id', undefined)
        params['region_type_id'] = self.get_argument('region_type_id', undefined)
        params['user_id'] = self.get_argument('user_id', undefined)
        params['dashboard_id'] = self.get_argument('dashboard_id', undefined)
        params['ttype'] = self.get_argument('ttype', undefined)
        publish = Publish.select(id=publish_id)
        publish = publish.update(**params)
        return SuccessData(
            publish.id
        )

    @BaseHandler.ajax_base()
    def delete(self, publish_id=None):
        publish = Publish.select(id=publish_id)
        publish.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
