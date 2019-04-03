# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Field.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Field import Field
from common.Utils.log_utils import getLogger

log = getLogger("views/Field")


class FieldHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, field_id=None):
        if field_id:
            field = Field.select(id=field_id)
            return Field.to_front()
        else:
            field_list = Field.filter()
            return [field.to_front() for field in field_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        field = Field.create(params)
        return field.to_front()

    @BaseHandler.ajax_base()
    def put(self, field_id):
        params = self.get_all_arguments()
        field = Field.select(id=field_id)
        field = field.update(params)
        return field.to_front()

    @BaseHandler.ajax_base()
    def patch(self, field_id):
        params = self.get_all_arguments()
        field = Field.select(id=field_id)
        field = field.update(params)
        return field.to_front()

    @BaseHandler.ajax_base()
    def delete(self, field_id):
        field = Field.select(id=field_id)
        field.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
