# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.ValueGroup import ValueGroup

log = getLogger("views/ValueGroup")


class ValueGroupHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, value_group_id=None):
        if value_group_id:
            value_group = ValueGroup.select(id=value_group_id)
            return value_group.to_front()
        else:
            value_group_list = ValueGroup.filter()
            return [value_group.to_front() for value_group in value_group_list]

    @BaseHandler.ajax_base()
    def post(self, value_group_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['value'] = self.get_argument('value', None)
        params['expression'] = self.get_argument('expression', None)
        value_group = ValueGroup.create(**params)
        return value_group.id

    @BaseHandler.ajax_base()
    def put(self, value_group_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['value'] = self.get_argument('value', None)
        params['expression'] = self.get_argument('expression', None)
        value_group = ValueGroup.select(id=value_group_id)
        value_group = value_group.update(**params)
        return value_group.id

    @BaseHandler.ajax_base()
    def patch(self, value_group_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['value'] = self.get_argument('value', undefined)
        params['expression'] = self.get_argument('expression', undefined)
        value_group = ValueGroup.select(id=value_group_id)
        value_group = value_group.update(**params)
        return value_group.id

    @BaseHandler.ajax_base()
    def delete(self, value_group_id=None):
        value_group = ValueGroup.select(id=value_group_id)
        value_group.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
