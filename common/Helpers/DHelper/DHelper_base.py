# -*- coding: utf-8 -*-
# @Author  : SWXS
# @File    : DHelper_base.py
# @Time    : 2018/2/28 15:04

import pandas as pd
from collections import namedtuple

Filter = namedtuple("Filter", ("column", "value", "option", "dtype"))
New_column = namedtuple("New_column", ("new_column", "column", "column_id", "column_ttype", "dtype", "date_type", "aggable", "agg_name", "multifunc"))
Drilldown_column = namedtuple("Drilldown_column", ("new_column", "value", "column_id", "dtype"))
Field_filter = namedtuple("Field_filter", ("new_column", "column", "value_list", "sort", "column_id", "dtype"))
Pivot_main = namedtuple("Pivot_main", ("new_column", "index_list", "aggable", "func", "multifunc", "sortfunc", "sort_regiontype_id"))
Pivot_sub = namedtuple("Pivot_sub", ("new_column", "index_list", "aggable", "func", "multifunc", "sortfunc", "sort_regiontype_id"))


class DHelper_base(object):
    """
    规范如何添加状态，如何输出状态
    :param args:
    :param kwargs:
    """

    def __init__(self, *args, **kwargs):
        self._filter_list = []
        self._new_column_list = []
        self._field_filter_list = []
        self._drilldown_list = []
        self._pivot_main_list = []
        self._pivot_sub_list = []
        self._pivot_main_x_list = []
        self._pivot_sub_x_list = []
        self._pivot_main_y_list = []
        self._pivot_sub_y_list = []

    def add_filter(self, column, value, option=None, dtype=None):
        self._filter_list.append(Filter(column, value, option, dtype))

    def add_new_column(self, new_column, column, column_id=None, column_ttype=None, dtype=None, date_type=None, aggable=True, agg_name=None, multifunc=None):
        self._new_column_list.append(New_column(new_column, column, column_id, column_ttype, dtype, date_type, aggable, agg_name, multifunc))

    def add_drilldown(self, new_column, value, column_id=None, dtype=None):
        self._drilldown_list.append(Drilldown_column(new_column, value, column_id, dtype))

    def add_field_filter(self, new_column, column, value_list, sort=False, column_id=None, dtype=None):
        self._field_filter_list.append(Field_filter(new_column, column, value_list, sort, column_id, dtype))

    def add_main_pivot(self, new_column, index_list, aggable=True, func=None, multifunc=None, sortfunc=None, sort_regiontype_id=None):
        self._pivot_main_list.append(Pivot_main(new_column, index_list, aggable, func, multifunc, sortfunc, sort_regiontype_id))

    def add_main_x_pivot(self, new_column, index_list, aggable=True, func=None, multifunc=None, sortfunc=None, sort_regiontype_id=None):
        self._pivot_main_x_list.append(Pivot_main(new_column, index_list, aggable, func, multifunc, sortfunc, sort_regiontype_id))

    def add_main_y_pivot(self, new_column, index_list, aggable=True, func=None, multifunc=None, sortfunc=None, sort_regiontype_id=None):
        self._pivot_main_y_list.append(Pivot_main(new_column, index_list, aggable, func, multifunc, sortfunc, sort_regiontype_id))

    def add_sub_pivot(self, new_column, index_list, aggable=True, func=None, multifunc=None, sortfunc=None, sort_regiontype_id=None):
        self._pivot_sub_list.append(Pivot_sub(new_column, index_list, aggable, func, multifunc, sortfunc, sort_regiontype_id))

    def add_sub_x_pivot(self, new_column, index_list, aggable=True, func=None, multifunc=None, sortfunc=None, sort_regiontype_id=None):
        self._pivot_sub_x_list.append(Pivot_sub(new_column, index_list, aggable, func, multifunc, sortfunc, sort_regiontype_id))

    def add_sub_y_pivot(self, new_column, index_list, aggable=True, func=None, multifunc=None, sortfunc=None, sort_regiontype_id=None):
        self._pivot_sub_y_list.append(Pivot_sub(new_column, index_list, aggable, func, multifunc, sortfunc, sort_regiontype_id))

    def do_preprocess(self):
        raise Exception('should be implimented in sub class')

    def do_pivot(self, has_color_tag, fillna="-"):
        raise Exception('should be implimented in sub class')

    def do_rank(self, dtype, ascending, sortIndex, xAxisCount=None):
        raise Exception('should be implimented in sub class')

    def do_refresh(self, field_id_list):
        raise Exception('should be implimented in sub class')

    def _get_head_name(self, df=None):
        if df.columns.name:
            return [df.columns.name]
        else:
            return list(df.columns.names)

    def _get_head_value(self, df=None):
        return df.columns.tolist()

    def _get_data_list(self, df=None, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(df))))
        return [
            dict(name=str(field_name), value=df.loc[field_name].tolist())
            for field_name in df.iloc[index_range].index.tolist()
        ]

    def get_pivot_data(self, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(self.pivot_df))))
        return self.pivot_df.iloc[index_range, :]

    def get_pivot_data_result(self, start=0, end=None):
        """
        以通用格式，返回聚合数据源， 常用于图表展示
        :param start:
        :param end:
        :return:
        """
        return dict(
            head=dict(name=self._get_head_name(df=self.pivot_df), value=self._get_head_value(df=self.pivot_df)),
            data=self._get_data_list(df=self.pivot_df, start=start, end=end),
            info=dict(length=len(self.pivot_df))
        )

    def get_pivot_group_data_result(self, color_tag=False, start=0, end=None):
        """
        以通用格式，返回聚合数据源， 常用于图表展示(散点图专用)
        :param color_tag:
        :param start:
        :param end:
        :return:
        """
        if color_tag:
            self.group_df = pd.concat([self.pivot_x_df, self.pivot_y_df])
            return dict(
                head=dict(name=self._get_head_name(df=self.group_df), value=self._get_head_value(df=self.group_df)),
                data=[
                    self._get_data_list(df=self.pivot_x_df, start=start, end=end),
                    self._get_data_list(df=self.pivot_y_df, start=start, end=end)
                ],
                info=dict(length=len(self.group_df))
            )
        else:
            return dict(
                head=dict(name=self._get_head_name(df=self.group_df), value=self._get_head_value(df=self.group_df)),
                data=self._get_data_list(df=self.group_df, start=start, end=end),
                info=dict(length=len(self.group_df))
            )

    def get_pivot_data_as_raw_data_result(self, start=0, end=None):
        """
        以通用格式，将聚合数据源以原始格式返回，去除聚合信息， 常用于下载数据源
        :param start:
        :param end:
        :return:
        """
        self.pivot_df = self.pivot_df.T.reset_index()
        return self.get_pivot_data_result(start=start, end=end)

    def get_pivot_group_data_as_raw_data_result(self, color_tag=False, start=0, end=None):
        """
        以通用格式，将聚合数据源以原始格式返回，去除聚合信息， 常用于下载数据源(散点图专用)
        :param color_tag:
        :param start:
        :param end:
        :return:
        """
        if color_tag:
            self.group_df = pd.concat([self.pivot_x_df, self.pivot_y_df])
            return dict(
                head=dict(name=self._get_head_name(df=self.group_df), value=self._get_head_value(df=self.group_df)),
                data=[
                    self._get_data_list(df=self.pivot_x_df, start=start, end=end),
                    self._get_data_list(df=self.pivot_y_df, start=start, end=end)
                ],
                info=dict(length=len(self.group_df))
            )
        else:
            self.group_df = self.group_df.T.reset_index()
            return self.get_pivot_group_data_result(start=start, end=end)

    async def get_raw_data_result(self, column_list, start=0, end=None):
        """
        以通用格式将未做聚合操作的数据源返回其中指定的部分数据列
        :param column_list: 指定的数据列
        :param start: 开始行数
        :param end: 结束行数
        :return:
        """
        index_range = slice(*(slice(start, end).indices(len(self.df))))
        self.pivot_df = self.df.reset_index().iloc[index_range, :].loc[:, column_list]
        result = self.get_pivot_data_result()
        result.update(dict(info=dict(length=len(self.df))))
        return result

    async def get_base_data(self, start=0, end=None):
        raise Exception('should be implimented in sub class')

    def get_field_unique_value_list(self, column, dtype):
        raise Exception('should be implimented in sub class')
