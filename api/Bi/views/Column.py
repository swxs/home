# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Column import Column
from common.Utils.log_utils import getLogger

log = getLogger("views/Column")


class ColumnHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, column_id=None):
        if column_id:
            column = Column.select(id=column_id)
            return Column.to_front()
        else:
            column_list = Column.filter()
            return [column.to_front() for column in column_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        column = Column.create(params)
        return column.to_front()

    @BaseHandler.ajax_base()
    def put(self, column_id):
        params = self.get_all_arguments()
        column = Column.select(id=column_id)
        column = column.update(params)
        return column.to_front()

    @BaseHandler.ajax_base()
    def patch(self, column_id):
        params = self.get_all_arguments()
        column = Column.select(id=column_id)
        column = column.update(params)
        return column.to_front()

    @BaseHandler.ajax_base()
    def delete(self, column_id):
        column = Column.select(id=column_id)
        column.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
