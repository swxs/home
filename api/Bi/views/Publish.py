# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Publish import Publish

log = getLogger("views/Publish")


class PublishHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, publish_id=None):
        if publish_id:
            publish = Publish.select(id=publish_id)
            return publish.to_front()
        else:
            publish_list = Publish.filter()
            return [publish.to_front() for publish in publish_list]

    @BaseHandler.ajax_base()
    def post(self, publish_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['region_id'] = self.get_argument('region_id', None)
        params['region_type_id'] = self.get_argument('region_type_id', None)
        params['user_id'] = self.get_argument('user_id', None)
        params['dashboard_id'] = self.get_argument('dashboard_id', None)
        params['ttype'] = self.get_argument('ttype', None)
        publish = Publish.create(**params)
        return publish.id

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
        return publish.id

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
        return publish.id

    @BaseHandler.ajax_base()
    def delete(self, publish_id=None):
        publish = Publish.select(id=publish_id)
        publish.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
