# -*- coding: utf-8 -*-
# @File    : Field.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Field import Field

log = getLogger("views/Field")


class FieldHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, field_id=None):
        if field_id:
            field = Field.select(id=field_id)
            return SuccessData(
                field.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            field_list = Field.search(**search_params).order_by()
            pager = Page(field_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, field_id=None):
        if field_id:
            params = dict()
            params['chart_id'] = self.get_argument('chart_id', undefined)
            params['name'] = self.get_argument('name', undefined)
            params['display_name'] = self.get_argument('display_name', undefined)
            params['column_id'] = self.get_argument('column_id', undefined)
            params['is_unique'] = self.get_argument('is_unique', undefined)
            params['agg_type'] = self.get_argument('agg_type', undefined)
            params['multi_agg_type'] = self.get_argument('multi_agg_type', undefined)
            params['sort_type'] = self.get_argument('sort_type', undefined)
            params['date_type'] = self.get_argument('date_type', undefined)
            params['sort_region_type_id'] = self.get_argument('sort_region_type_id', undefined)
            params['ttype'] = self.get_argument('ttype', undefined)
            params['dtype'] = self.get_argument('dtype', undefined)
            params['stype'] = self.get_argument('stype', undefined)
            params['range_region_type_id'] = self.get_argument('range_region_type_id', undefined)
            params['custom_attr'] = self.get_argument('custom_attr', undefined)
            field = Field.select(id=field_id)
            field = field.copy(**params)
            return SuccessData(
                field.id
            )
        else:
            params = dict()
            params['chart_id'] = self.get_argument('chart_id', None)
            params['name'] = self.get_argument('name', None)
            params['display_name'] = self.get_argument('display_name', None)
            params['column_id'] = self.get_argument('column_id', None)
            params['is_unique'] = self.get_argument('is_unique', None)
            params['agg_type'] = self.get_argument('agg_type', None)
            params['multi_agg_type'] = self.get_argument('multi_agg_type', None)
            params['sort_type'] = self.get_argument('sort_type', None)
            params['date_type'] = self.get_argument('date_type', None)
            params['sort_region_type_id'] = self.get_argument('sort_region_type_id', None)
            params['ttype'] = self.get_argument('ttype', None)
            params['dtype'] = self.get_argument('dtype', None)
            params['stype'] = self.get_argument('stype', None)
            params['range_region_type_id'] = self.get_argument('range_region_type_id', None)
            params['custom_attr'] = self.get_argument('custom_attr', None)
            field = Field.create(**params)
            return SuccessData(
                field.id
            )

    @BaseHandler.ajax_base()
    def put(self, field_id=None):
        params = dict()
        params['chart_id'] = self.get_argument('chart_id', None)
        params['name'] = self.get_argument('name', None)
        params['display_name'] = self.get_argument('display_name', None)
        params['column_id'] = self.get_argument('column_id', None)
        params['is_unique'] = self.get_argument('is_unique', None)
        params['agg_type'] = self.get_argument('agg_type', None)
        params['multi_agg_type'] = self.get_argument('multi_agg_type', None)
        params['sort_type'] = self.get_argument('sort_type', None)
        params['date_type'] = self.get_argument('date_type', None)
        params['sort_region_type_id'] = self.get_argument('sort_region_type_id', None)
        params['ttype'] = self.get_argument('ttype', None)
        params['dtype'] = self.get_argument('dtype', None)
        params['stype'] = self.get_argument('stype', None)
        params['range_region_type_id'] = self.get_argument('range_region_type_id', None)
        params['custom_attr'] = self.get_argument('custom_attr', None)
        field = Field.select(id=field_id)
        field = field.update(**params)
        return SuccessData(
            field.id
        )

    @BaseHandler.ajax_base()
    def patch(self, field_id=None):
        params = dict()
        params['chart_id'] = self.get_argument('chart_id', undefined)
        params['name'] = self.get_argument('name', undefined)
        params['display_name'] = self.get_argument('display_name', undefined)
        params['column_id'] = self.get_argument('column_id', undefined)
        params['is_unique'] = self.get_argument('is_unique', undefined)
        params['agg_type'] = self.get_argument('agg_type', undefined)
        params['multi_agg_type'] = self.get_argument('multi_agg_type', undefined)
        params['sort_type'] = self.get_argument('sort_type', undefined)
        params['date_type'] = self.get_argument('date_type', undefined)
        params['sort_region_type_id'] = self.get_argument('sort_region_type_id', undefined)
        params['ttype'] = self.get_argument('ttype', undefined)
        params['dtype'] = self.get_argument('dtype', undefined)
        params['stype'] = self.get_argument('stype', undefined)
        params['range_region_type_id'] = self.get_argument('range_region_type_id', undefined)
        params['custom_attr'] = self.get_argument('custom_attr', undefined)
        field = Field.select(id=field_id)
        field = field.update(**params)
        return SuccessData(
            field.id
        )

    @BaseHandler.ajax_base()
    def delete(self, field_id=None):
        field = Field.select(id=field_id)
        field.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")