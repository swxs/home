# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.ValueGroup import ValueGroup
from common.Utils.log_utils import getLogger

log = getLogger("views/ValueGroup")


class ValueGroupHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, value_group_id=None):
        if value_group_id:
            value_group = ValueGroup.select(id=value_group_id)
            return ValueGroup.to_front()
        else:
            value_group_list = ValueGroup.filter()
            return [value_group.to_front() for value_group in value_group_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        value_group = ValueGroup.create(params)
        return value_group.to_front()

    @BaseHandler.ajax_base()
    def put(self, value_group_id):
        params = self.get_all_arguments()
        value_group = ValueGroup.select(id=value_group_id)
        value_group = value_group.update(params)
        return value_group.to_front()

    @BaseHandler.ajax_base()
    def patch(self, value_group_id):
        params = self.get_all_arguments()
        value_group = ValueGroup.select(id=value_group_id)
        value_group = value_group.update(params)
        return value_group.to_front()

    @BaseHandler.ajax_base()
    def delete(self, value_group_id):
        value_group = ValueGroup.select(id=value_group_id)
        value_group.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
