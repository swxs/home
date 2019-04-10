# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Datafilter import Datafilter

log = getLogger("views/Datafilter")


class DatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datafilter_id=None):
        if datafilter_id:
            datafilter = Datafilter.select(id=datafilter_id)
            return datafilter.to_front()
        else:
            datafilter_list = Datafilter.filter()
            return [datafilter.to_front() for datafilter in datafilter_list]

    @BaseHandler.ajax_base()
    def post(self, datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['column_id'] = self.get_argument('column_id', None)
        params['worktable_id'] = self.get_argument('worktable_id', None)
        params['dtype'] = self.get_argument('dtype', None)
        params['custom_attr'] = self.get_argument('custom_attr', None)
        datafilter = Datafilter.create(**params)
        return datafilter.id

    @BaseHandler.ajax_base()
    def put(self, datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['column_id'] = self.get_argument('column_id', None)
        params['worktable_id'] = self.get_argument('worktable_id', None)
        params['dtype'] = self.get_argument('dtype', None)
        params['custom_attr'] = self.get_argument('custom_attr', None)
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter = datafilter.update(**params)
        return datafilter.id

    @BaseHandler.ajax_base()
    def patch(self, datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['column_id'] = self.get_argument('column_id', undefined)
        params['worktable_id'] = self.get_argument('worktable_id', undefined)
        params['dtype'] = self.get_argument('dtype', undefined)
        params['custom_attr'] = self.get_argument('custom_attr', undefined)
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter = datafilter.update(**params)
        return datafilter.id

    @BaseHandler.ajax_base()
    def delete(self, datafilter_id=None):
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
