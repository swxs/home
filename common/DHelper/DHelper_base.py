# -*- coding: utf-8 -*-
# @Author  : SWXS
# @File    : DHelper_base.py
# @Time    : 2018/2/28 15:04

from collections import namedtuple

from common.Utils import df_utils

Filter = namedtuple("Filter", ("column", "value_list", "dtype"))
New_column = namedtuple("New_column", ("new_column", "column", "dtype", "dategroup", "aggable", "agg_name", "multifunc"))
Drilldown_column = namedtuple("Drilldown_column", ("new_column", "value"))
Field_filter = namedtuple("Field_filter", ("new_column", "column", "value_list", "sort"))
Pivot_main = namedtuple("Pivot_main", ("new_column", "index_list", "aggable", "func", "multifunc", "sortfunc", "sort_regiontype_id"))
Pivot_sub = namedtuple("Pivot_sub", ("new_column", "index_list", "aggable", "func", "multifunc", "sortfunc", "sort_regiontype_id"))


class DHelper_base(object):
    def __new__(cls, *args):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.__singleton__ = singleton = object.__new__(cls)
        return singleton

    def __init__(self, df=None, project_id=None):
        self._filter_list = []
        self._new_column_list = []
        self._field_filter_list = []
        self._drilldown_list = []
        self._pivot_main_list = []
        self._pivot_sub_list = []

    def add_filter(self, column, value_list, dtype=None):
        self._filter_list.append(Filter(column, value_list, dtype))

    def add_new_column(self, new_column, column, dtype=None, dategroup=None, aggable=True, agg_name=None, multifunc=None):
        self._new_column_list.append(New_column(new_column, column, dtype, dategroup, aggable, agg_name, multifunc))

    def add_drilldown(self, new_column, value):
        self._drilldown_list.append(Drilldown_column(new_column, value))

    def add_field_filter(self, new_column, column, value_list, sort=False):
        self._field_filter_list.append(Field_filter(new_column, column, value_list, sort))

    def add_main_pivot(self, new_column, index_list, aggable=True, func=None, multifunc=None, sortfunc=None, sort_regiontype_id=None):
        self._pivot_main_list.append(Pivot_main(new_column, index_list, aggable, func, multifunc, sortfunc, sort_regiontype_id))

    def add_sub_pivot(self, new_column, index_list, aggable=True, func=None, multifunc=None, sortfunc=None, sort_regiontype_id=None):
        self._pivot_sub_list.append(Pivot_sub(new_column, index_list, aggable, func, multifunc, sortfunc, sort_regiontype_id))

    def get_base_data(self):
        raise Exception('should be implimented in sub class')

    def do_preprocess(self):
        raise Exception('should be implimented in sub class')

    def do_pivot(self, has_colortag, fillna="-"):
        raise Exception('should be implimented in sub class')

    def do_rank(self, dtype, ascending, sortIndex, xAxisCount=None):
        raise Exception('should be implimented in sub class')

    def do_refresh(self, field_id_list):
        raise Exception('should be implimented in sub class')

    def get_pivot_data_result(self, start=0, end=None):
        """
        case N_INDEX_N_COLOR_1_VALUE:
        'head': {'name': ['All'], 'value': ['All']}
        'data': [{'name': '5a4c3a5cfdcf231d104db135', 'value': [332623]}]
        'info': {'length': 1}

        case 1_INDEX_N_COLOR_1_VALUE:
        'head': {'name': ['5a56c77bfdcf23104cffacdb'], 'value': [1L, 2L, 3L]}
        'data': [{'name': '5a4c3a5cfdcf231d104db135', 'value': [98159, 225832, 8632]}]
        'info': {'length': 1}

        case 2_INDEX_N_COLOR_1_VALUE:
        'head': {'name': FrozenList(['5a56c77bfdcf23104cffacdb', '5a56c7dafdcf23104cffacdc']), 'value': [(1L, 1.0), (1L, 2.0), (1L, 3.0), (1L, 4.0), (1L, 5.0), (1L, 6.0), (2L, 1.0), (2L, 2.0), (2L, 3.0), (2L, 4.0), (2L, 5.0), (2L, 6.0), (3L, 1.0), (3L, 2.0), (3L, 3.0),
        'data': [{'name': '5a4c3a5cfdcf231d104db135', 'value': [54241, 35875, 1139, 512, 1152, 5240, 138090, 71712, 2201, 600, 2793, 10436, 5435, 2603, 87, 296, 79, 132]}]
        'info': {'length': 1}
        """
        raise Exception('should be implimented in sub class')

    def get_pivot_data_as_raw_data_result(self, start=0, end=None):
        raise Exception('should be implimented in sub class')

    def get_raw_data_result(self, index_list, start=0, end=None):
        raise Exception('should be implimented in sub class')

    def get_field_unique_value_list(self, column_name, dtype):
        raise Exception('should be implimented in sub class')
