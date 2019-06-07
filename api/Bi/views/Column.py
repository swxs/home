# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Column import Column

log = getLogger("views/Column")


class ColumnHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, column_id=None):
        if column_id:
            column = Column.select(id=column_id)
            return SuccessData(
                column.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            column_list = Column.search(**search_params).order_by()
            pager = Page(column_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, column_id=None):
        if column_id:
            params = dict()
            params['col'] = self.get_argument('col', undefined)
            params['realcol'] = self.get_argument('realcol', undefined)
            params['readablecol'] = self.get_argument('readablecol', undefined)
            params['worktable_id'] = self.get_argument('worktable_id', undefined)
            params['is_visible'] = self.get_argument('is_visible', undefined)
            params['is_unique'] = self.get_argument('is_unique', undefined)
            params['dtype'] = self.get_argument('dtype', undefined)
            params['ttype'] = self.get_argument('ttype', undefined)
            params['expression'] = self.get_argument('expression', undefined)
            params['value_group_id_list'] = self.get_argument('value_group_id_list', undefined)
            column = Column.select(id=column_id)
            column = column.copy(**params)
            return SuccessData(
                column.id
            )
        else:
            params = dict()
            params['col'] = self.get_argument('col', None)
            params['realcol'] = self.get_argument('realcol', None)
            params['readablecol'] = self.get_argument('readablecol', None)
            params['worktable_id'] = self.get_argument('worktable_id', None)
            params['is_visible'] = self.get_argument('is_visible', None)
            params['is_unique'] = self.get_argument('is_unique', None)
            params['dtype'] = self.get_argument('dtype', None)
            params['ttype'] = self.get_argument('ttype', None)
            params['expression'] = self.get_argument('expression', None)
            params['value_group_id_list'] = self.get_argument('value_group_id_list', None)
            column = Column.create(**params)
            return SuccessData(
                column.id
            )

    @BaseHandler.ajax_base()
    def put(self, column_id=None):
        params = dict()
        params['col'] = self.get_argument('col', None)
        params['realcol'] = self.get_argument('realcol', None)
        params['readablecol'] = self.get_argument('readablecol', None)
        params['worktable_id'] = self.get_argument('worktable_id', None)
        params['is_visible'] = self.get_argument('is_visible', None)
        params['is_unique'] = self.get_argument('is_unique', None)
        params['dtype'] = self.get_argument('dtype', None)
        params['ttype'] = self.get_argument('ttype', None)
        params['expression'] = self.get_argument('expression', None)
        params['value_group_id_list'] = self.get_argument('value_group_id_list', None)
        column = Column.select(id=column_id)
        column = column.update(**params)
        return SuccessData(
            column.id
        )

    @BaseHandler.ajax_base()
    def patch(self, column_id=None):
        params = dict()
        params['col'] = self.get_argument('col', undefined)
        params['realcol'] = self.get_argument('realcol', undefined)
        params['readablecol'] = self.get_argument('readablecol', undefined)
        params['worktable_id'] = self.get_argument('worktable_id', undefined)
        params['is_visible'] = self.get_argument('is_visible', undefined)
        params['is_unique'] = self.get_argument('is_unique', undefined)
        params['dtype'] = self.get_argument('dtype', undefined)
        params['ttype'] = self.get_argument('ttype', undefined)
        params['expression'] = self.get_argument('expression', undefined)
        params['value_group_id_list'] = self.get_argument('value_group_id_list', undefined)
        column = Column.select(id=column_id)
        column = column.update(**params)
        return SuccessData(
            column.id
        )

    @BaseHandler.ajax_base()
    def delete(self, column_id=None):
        column = Column.select(id=column_id)
        column.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
