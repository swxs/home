# coding=utf8

import os
import math
import json
import datetime
from itertools import zip_longest

import numpy as np
import pandas as pd
from tornado.util import ObjectDict

from apps.errors import AppResourceError
from commons.Helpers.Helper_Excel import Dataframe_Excel_Helper

try:
    from pandas._libs.tslibs.nattype import NaTType
except:
    from pandas._libs.tslibs import NaTType

try:
    Period = pd.Period
except AttributeError:
    Period = pd._libs.period.Period

import settings
from exceptions import ResourceError
from commons import consts
from commons.color_utils import Color
from commons import log_utils
from commons.translation_utils import get_translate_and_code
from commons.DHelper.DHelper_base import Pivot_main
from commons.Helpers.Helper_validate import Validate, RegType
from commons.Echarts.option_serie import get_base_series_option
from commons.Echarts.option_consts import *
from commons.Echarts.option_chart import (
    color,
    get_base_chart_option,
    double_x_grid,
    double_y_grid,
    index_axis,
    value_axis,
    visualmap_piecewise,
    visualmap_continuous,
)
from apps.bi import model_enums
from apps.bi import chart_enums
from apps.bi import worktable_utils
from apps.bi import field_utils
from apps.bi import column_utils
from apps.bi import chart_utils

logger = log_utils.get_logging(name='model', file_name='model.log')


class Vtype:
    N_VALUE_N_COLOR_N_INDEX = 0  # 不出图
    N_VALUE_N_COLOR_Y_INDEX = 1  # 不出图
    N_VALUE_Y_COLOR_N_INDEX = 2  # 不出图
    N_VALUE_Y_COLOR_Y_INDEX = 3  # 不出图
    Y_VALUE_N_COLOR_N_INDEX = 4  # 1栏 全体数据处理             [度量]
    Y_VALUE_N_COLOR_Y_INDEX = 5  # n栏 全体数据处理             [度量]
    Y_VALUE_Y_COLOR_N_INDEX = 6  # 1栏 全体数据根据对比拆分1个度量 [对比]
    Y_VALUE_Y_COLOR_Y_INDEX = 7  # n栏 全体数据根据对比拆分1个度量 [对比]


def _get_word_count(unicode_str):
    count = 0
    for c in unicode_str:
        if ord(c) < 128:
            count += 1
        else:
            count += 2
    return count


class BaseChart(object):
    # name = "base"  # 注释掉避免从子类取到该 name 导致错误

    def __init__(self, dbchart, dh, **params):
        self.dbchart = dbchart
        self.dh = dh

        self.params = params
        self.realtime_filter = params.get('realtime_filter', dict())
        self.data_filter_list = self.realtime_filter.get("data_filter_list", [])
        self.drilldown_list = self.realtime_filter.get("drilldown_list", [])
        self.ascending = self.realtime_filter.get('ascending', None)
        self.sort_index = self.realtime_filter.get('sort_index', 0)
        self.custom_attr = self.realtime_filter.get('custom_attr', dict())
        self.value_field_id_list = self.realtime_filter.get('value_field_id_list', [])

        self.group_id_list = params.get('group_id_list', [])
        self.locale = self.params.get('locale', None)
        self._, self.code = get_translate_and_code(self.locale)

        self._color_series_list = list()
        self.axis_data_list = []
        self.legend_data_list = []

        self.option = None
        self.chart_option = dict(
            show_type="echart"
        )
        self.formatterDict = dict()

    async def create(self, chart):
        # 这里虽好把所有信息拿到， 后边直接取， 不然可能会有多次取值不一致的情况
        worktable = await worktable_utils.get_worktable(chart.worktable_id)

        self.field_list = await field_utils.get_field_list_with_chart_id(chart.oid)
        self.all_field_list = self.field_list[:] + [await field_utils.get_field(field_id) for field_id in self.value_field_id_list]
        self.index_list = [field for field in self.all_field_list if field.stype == model_enums.FIELD_STYPE_INDEX]
        self.value_list = [field for field in self.all_field_list if field.stype == model_enums.FIELD_STYPE_VALUE]
        self.value_x_list = [field for field in self.all_field_list if field.stype == model_enums.FIELD_STYPE_VALUE_X]
        self.value_y_list = [field for field in self.all_field_list if field.stype == model_enums.FIELD_STYPE_VALUE_Y]
        self.sub_value_list = [field for field in self.all_field_list if field.stype == model_enums.FIELD_STYPE_SUB_VALUE]
        self.grid_value_list = [field for field in self.all_field_list if field.stype == model_enums.FIELD_STYPE_GRID_VALUE]
        self.color_value_list = [field for field in self.all_field_list if field.stype == model_enums.FIELD_STYPE_COLOR_VALUE]
        self.colortag_list = [field for field in self.all_field_list if field.stype == model_enums.FIELD_STYPE_COLORTAG]
        if self.colortag_list:
            self.colortag = self.colortag_list[0]
        else:
            self.colortag = None

        self.value_field_group = list(zip_longest(
            (field.id for field in self.value_x_list),
            (field.id for field in self.value_y_list)
        ))

        self.vtype = self._get_vtype()

    def _has_value(self):
        return (self.vtype & 4) > 0

    def _has_color(self):
        return (self.vtype & 2) > 0

    def _has_index(self):
        return (self.vtype & 1) > 0

    def _has_color_tag(self):
        return bool(self.colortag)

    def _has_visual_map(self, field_id):
        if self.colortag is not None:
            return False
        for field in self.value_list:
            if field_id == field.id:
                return True
        for field in self.sub_value_list:
            if field_id == field.id:
                return True
        for field in self.value_x_list:
            if field_id == field.id:
                return True
        for field in self.value_y_list:
            if field_id == field.id:
                return True
        for field in self.grid_value_list:
            if field_id == field.id:
                return True
        return False

    async def _is_index(self, field_id):
        if field_id is None:
            return False
        if Validate.check(field_id, reg_type=RegType.COLUMN_ID):
            field = await field_utils.get_field(field_id)
            if field.stype == model_enums.FIELD_STYPE_INDEX:
                return True
        return False

    async def _convert_field_name(self, field_id):
        """
        将field_id转换成对应的名字, 常用于将维度id转换为文字
        :param field_id: 一般是field_id, 可能是对比字段的值， 可能是All
        :return:
        """
        params = ObjectDict(
            chart_id=self.dbchart.oid
        )
        field_list = await field_utils.get_field_list(params)
        if "\001" in field_id:
            value_field_id, colortag_value = field_id.split("\001")
            field = await field_utils.get_field(value_field_id)
            colortag_part = await self._convert_colortag_value(colortag_value)
            if len(self.value_list) + len(self.sub_value_list) > 1:
                if field.display_name:
                    return f"{self._(field.display_name)}-{colortag_part}"
                else:
                    return f"{self._(field.name)}-{colortag_part}"
            else:
                return colortag_part
        elif (
                    Validate.check(field_id, reg_type=RegType.COLUMN_ID) and
                    (
                                (field_id in self.value_field_id_list) or
                                (field_id in (field.id for field in field_list))
                    )
        ):
            field = await field_utils.get_field(field_id)
            if field.display_name:
                return self._(field.display_name)
            else:
                return self._(field.name)
        else:
            return await self._convert_colortag_value(field_id)

    async def _convert_colortag_value(self, value):
        """
        将colortag的值转换成对应的值/映射值
        :param value: 可能是对比字段的值，可能是All
        :return:
        """
        if self.colortag is not None:
            column = await column_utils.get_column(self.colortag.column_id)
            return str(value)
        else:
            return str(value)

    async def _convert_column_value(self, value, field_id=None, field_list=None):
        """
        将维度值转换成映射的文字
        :param value:
        :param field_id:
        :param field_list:
        :return:
        """
        if field_list and len(field_list) == 1:
            field_id = field_list[0]
        if isinstance(value, (tuple, list)):
            changed_index_list = [await self._convert_column_value(x, field_id=field_list[i]) for i, x in enumerate(value)]
            key = reversed(changed_index_list)
            name = '\n'.join(key)
            return name
        else:
            return self._convert_string_value(value)

    async def _convert_column_value_dict(self, value, field_id=None, field_list=None):
        if field_list and len(field_list) == 1:
            field_id = field_list[0]
        if isinstance(value, tuple):
            changed_index_list = [await self._convert_column_value_dict(x, field_id=field_list[i]) for i, x in enumerate(value)]
            base_changed_index_list = [x.get(consts.BASE_LOCALE) for x in changed_index_list]
            base_key = reversed(base_changed_index_list)
            base_name = '\n'.join(base_key)
            code_changed_index_list = [x.get(self.code) for x in changed_index_list]
            code_key = reversed(code_changed_index_list)
            code_name = '\n'.join(code_key)
            return {consts.BASE_LOCALE: base_name, self.code: code_name}
        else:
            value = self._convert_string_value(value)
            return {consts.BASE_LOCALE: value, self.code: self._(value)}

    def _convert_string_value(self, value):
        """
        将值处理成字符串
        :param index:
        :return:
        """
        if isinstance(value, (tuple, list)):
            changed_index_list = [self._convert_string_value(x) for x in value]
            key = reversed(changed_index_list)
            name = '\n'.join(key)
        elif isinstance(value, (int, np.int, np.int8, np.int16, np.int32, np.int64)):
            name = str(value)
        elif isinstance(value, (float, np.float, np.float16, np.float32, np.float64)):
            if math.isnan(value):
                name = settings.NONE_DATA
            elif np.isinf(value):
                name = settings.NONE_DATA
            else:
                name = str(value)
                # name = index.replace("nan", settings.NONE_DATA)
        elif isinstance(value, datetime.datetime):
            if isinstance(value, NaTType):
                name = settings.NONE_DATA
            else:
                name = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.date):
            if isinstance(value, NaTType):
                name = settings.NONE_DATA
            else:
                name = value.strftime('%Y-%m-%d 00:00:00')
        else:
            try:
                name = str(value)
            except Exception as e:
                logger.exception(f"index: {value}, with type: {type(value)} can`t be str convert!"),
                name = str(value)
        return name

    def _convert_number_value(self, value):
        if isinstance(value, (np.float, np.float16, np.float32, np.float64)):
            if math.isnan(value):
                value = settings.NONE_DATA
            elif np.isinf(value):
                value = settings.NONE_DATA
        return value

    async def _get_drilldown_info(self):
        if self.dbchart.is_drilldown and hasattr(self, 'drilldown_field_id'):
            field = await field_utils.get_field(self.drilldown_field_id)
            column = await column_utils.get_column(field.column_id)
            self.drill_down_info = [
                await self._convert_column_value_dict(value, field_id=self.drilldown_field_id)
                for value in self.dh.get_field_unique_value_list(column, dtype=column.dtype)
            ]
        else:
            self.drill_down_info = []
        return self.drill_down_info

    def _get_color_list(self, color):
        if color is None:
            return None
        else:
            return Color.get_color_list(color)

    def _get_series_data_list(self, data_list):
        return [data if not isinstance(data, dict) else data.get('value') for data in data_list]

    def _get_color(self, data_list, color_min=None, color_max=None):
        if color_min is None:
            color_min = self._get_color_list(DEFAULT_MIN_COLOR)
        if color_max is None:
            color_max = self._get_color_list(DEFAULT_MAX_COLOR)
        color_list = []
        tmp_data_list = [data if data not in ["-", float("inf"), float("-inf")] else 0 for data in data_list]
        if tmp_data_list:
            min_data, max_data = min(tmp_data_list), max(tmp_data_list)
            for data in tmp_data_list:
                _color_list = []
                if max_data - min_data == 0:
                    for index, (_color_min, _color_max) in enumerate(zip(color_min, color_max)):
                        if index > 2:
                            _color = (_color_min + _color_max) / 2
                        else:
                            _color = (_color_min + _color_max) // 2
                        _color_list.append(_color)
                else:
                    for index, (_color_min, _color_max) in enumerate(zip(color_min, color_max)):
                        if index > 2:
                            _color = (data * _color_max - data * _color_min + max_data * _color_min - min_data * _color_max) / (max_data - min_data)
                        else:
                            _color = int((data * _color_max - data * _color_min + max_data * _color_min - min_data * _color_max) / (max_data - min_data))
                        _color_list.append(_color)
                color_list.append(f"rgba({', '.join([str(c) for c in _color_list])})")
        return color_list

    async def get_filtered_df(self, ttype=chart_enums.CHART_DISPLAY_SHOW):
        await chart_utils.get_changed_df(
            self.dbchart,
            self.dh,
            self.all_field_list,
            realtime_filter=self.realtime_filter,
            group_id_list=self.group_id_list,
            ttype=ttype
        )
        self.dh.do_preprocess()

    @classmethod
    def delete_df_already_used_column(self, func):
        async def inner(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)
            params = ObjectDict(
                chart_id=self.dbchart.oid,
            )
            field_list = await field_utils.get_field_list(params)
            field_id_list = [field.id for field in field_list]
            self.dh.do_refresh(field_id_list)
            return result

        return inner

    def _get_vtype(self):
        # 计算类型
        vtype = 0
        if len(self.value_list) != 0 or len(self.value_x_list) != 0 or len(self.value_y_list) != 0 or len(self.value_field_id_list) != 0:
            vtype += 4
        if self.colortag is not None:
            vtype += 2
        if len(self.index_list) != 0:
            vtype += 1
        return vtype

    async def get_index(self, ttype=chart_enums.CHART_DISPLAY_SHOW, level=None):
        if ttype == chart_enums.CHART_DISPLAY_SHOW and self.dbchart.is_drilldown:
            self.drilldown_level = len(self.drilldown_list)
            if self.drilldown_level >= len(self.index_list):
                raise ResourceError(code=AppResourceError.NotFound, msg='钻取深度过深!')
            self.drilldown_field_id = self.index_list[self.drilldown_level].id
            self.sub_index = [self.index_list[self.drilldown_level].id]
            self.index_list = [self.index_list[self.drilldown_level]]
        else:
            if level is not None:
                self.sub_index = [x.id for i, x in enumerate(self.index_list) if i <= level]
            else:
                self.sub_index = [x.id for x in self.index_list]

        self.main_index = []
        self.main_index = self.sub_index[:]
        if self.colortag is not None:
            self.main_index.append(self.colortag.id)

        if len(self.sub_index) == 0:
            self.sub_index = [settings.COLUMN_ALL, ]
        if len(self.main_index) == 0:
            self.main_index = [settings.COLUMN_ALL, ]
        return self.main_index, self.sub_index

    def get_field_sort(self, field):
        if field.sort_type == model_enums.FIELD_SORT_TYPE_NONE:
            sort = None
        elif field.sort_type == model_enums.FIELD_SORT_TYPE_ASC:
            sort = True
        elif field.sort_type == model_enums.FIELD_SORT_TYPE_DESC:
            sort = False
        else:
            sort = None
        return sort

    async def _convert_field_to_main_pivot(self, field):
        column = await column_utils.get_column(field.column_id)
        if column.aggable:
            return field.id, self.main_index, column.aggable, field.agg_type, field.multi_agg_type, self.get_field_sort(field), field.sort_region_type_id
        else:
            return field.id, self.main_index, column.aggable, await column_utils.get_col_expression(column), field.multi_agg_type, self.get_field_sort(field), field.sort_region_type_id

    async def _convert_field_to_sub_pivot(self, field):
        column = await column_utils.get_column(field.column_id)
        if column.aggable:
            return field.id, self.sub_index, column.aggable, field.agg_type, field.multi_agg_type, self.get_field_sort(field), field.sort_region_type_id
        else:
            return field.id, self.main_index, column.aggable, await column_utils.get_col_expression(column), field.multi_agg_type, self.get_field_sort(field), field.sort_region_type_id

    async def get_df(self, fillna=settings.NONE_DATA, ttype=chart_enums.CHART_DISPLAY_SHOW):
        for field in self.value_list:
            self.dh.add_main_pivot(*await self._convert_field_to_main_pivot(field))

        for field in self.value_x_list:
            self.dh.add_main_x_pivot(*await self._convert_field_to_main_pivot(field))

        for field in self.value_y_list:
            self.dh.add_main_y_pivot(*await self._convert_field_to_main_pivot(field))

        for field in self.sub_value_list:
            if self.dbchart.custom_attr.get("split_sub_value", False):
                self.dh.add_main_pivot(*await self._convert_field_to_main_pivot(field))
            else:
                self.dh.add_sub_pivot(*await self._convert_field_to_sub_pivot(field))

        if self.dbchart.custom_attr and self.dbchart.custom_attr.get('has_grid', False):
            for field in self.grid_value_list:
                self.dh.add_sub_pivot(*await self._convert_field_to_sub_pivot(field))

        if (ttype != chart_enums.CHART_DISPLAY_DOWNLOAD) and (self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_COLOR_VALUE):
            if len(self.color_value_list) > 0:
                self.dh.add_sub_pivot(*await self._convert_field_to_sub_pivot(self.color_value_list[0]))

        await self.dh.do_pivot(self._has_color_tag(), fillna=fillna)

    async def get_ranked_df(self):
        """
        对数据做排序， 限制等操作
        :return:
        """
        if self.dbchart.custom_attr is not None and self.dbchart.custom_attr.get("showChartSort", False):
            if self._has_index() and self._has_value():
                # 有维度， 度量的场合
                d_type = 1
            elif self._has_value():
                # 只有度量的场合
                d_type = 2
            else:
                d_type = 0

            if self.ascending:
                ascending = self.ascending == "asc"
            else:
                ascending = (self.dbchart.custom_attr.get("sortType", "desc") == "asc")

            if self.dbchart.custom_attr.get("xAxisLimit", False):
                x_axis_count = self.dbchart.custom_attr.get("xAxisCount", None)
            else:
                x_axis_count = None

            self.dh.do_rank(d_type, ascending, self.sort_index, x_axis_count)

    async def get_pivot_df(self):
        if not self._has_value():
            return False
        else:
            await self.get_df()
            return True

    async def get_series_list(self):
        """
        数据层转换为配置
        :return:
        """
        series_list = []
        result = self.dh.get_pivot_data_result()

        for x in result["head"]["value"]:
            value = await self._convert_column_value(x, field_list=result["head"]["name"])
            self.axis_data_list.append(value)

        self.legend_data_list = []
        for data in result["data"]:
            index_name = await self._convert_field_name(data["name"])
            if "\001" in data["name"]:
                field_id, _ = data["name"].split("\001") # _ : colortag_value
            else:
                field_id = data["name"]
            series_option = None
            if field_id in (x.id for x in self.sub_value_list):
                """
                    从轴类型字段， 目前设置：
                    1.设置legend为直线
                    2.设置字段颜色
                """
                field = await field_utils.get_field(field_id)
                series_option = self.get_base_series_option(ttype=field.ttype)
                self.legend_data_list.append({"name": index_name, "icon": "line"})
                series_option.yAxisIndex = 1
            elif field_id in (x.id for x in self.grid_value_list):
                """
                    子图类型字段， 目前设置：
                    1.设置字段颜色
                    2.修改子图所处的X, Y轴序号
                """
                field = await field_utils.get_field(field_id)
                series_option = self.get_base_series_option(ttype=field.ttype)
                if field.custom_attr.get('color', None):
                    series_option.itemStyle.normal.color = field.custom_attr.get('color', None)
                series_option.xAxisIndex = len(self.option.xAxis) - 1
                series_option.yAxisIndex = len(self.option.yAxis) - 1
            elif field_id in (x.id for x in self.color_value_list):
                self._color_series_list.append({
                    "field_id": field_id,
                    "name": index_name,
                    "data": [self._convert_number_value(value) for value in data["value"]]
                })
            else:
                series_option = self.get_base_series_option()
                try:
                    field = await field_utils.get_field(field_id)
                    pieces = (self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_VALUE) and (field.custom_attr.get('advanced_color_type', None) == chart_enums.CHART_VMTYPE_PIECEWISE)
                except Exception as e:
                    pieces = False
                self.legend_data_list.append({"name": index_name, "pieces": pieces})

            if series_option:
                series_option.data = [
                    {"value": self._convert_number_value(value)}
                    for value in data["value"]
                ]
                series_option.field_id = data["name"]
                series_option.id = data["name"]
                series_option.name = index_name
                series_list.append(series_option)
        self.option.series = series_list

    def change_series_percent(self, fillna="-"):
        # TODO 这个函数的处理不通用
        """
        :param fillna:
        :return:
        """
        data_all = []
        if len(self.option.series) == 0:
            raise ResourceError(AppResourceError.NoData, "数据为空!")
        for _ in range(len(self.option.series[0].data)):
            data_all.append(0)
        for series in self.option.series:
            for i, data in enumerate(series.data):
                if data["value"] != fillna:
                    data_all[i] += data["value"]
        for series in self.option.series:
            for i, data in enumerate(series.data):
                if data["value"] != fillna:
                    series.data[i]["value"] = data["value"] / float(data_all[i])
                else:
                    series.data[i]["value"] = fillna

    async def to_option(self):
        raise Exception('should be implimented in sub class')

    async def _get_rawdata_export_headers(self, result):
        return [await self._convert_field_name(x) for x in result["head"]["value"]]

    async def _get_rawdata_export_datas(self, result):
        rawdata_export_datas = list()
        for data in result["data"]:
            data_list = list()
            for i, value in enumerate(data["value"]):
                data_list.append(await self._convert_column_value(value, field_id=result["head"]["value"][i]))
            rawdata_export_datas.append(data_list)
        return rawdata_export_datas

    async def to_base_data(self):
        base_data = self.dh.get_base_data()
        return base_data

    async def to_export_data(self):
        await self.create(self.dbchart)

        info_list = list()
        try:
            if self.dbchart.next_chart_id is not None:
                old_value_list = self.value_list
                self.dbchart = await chart_utils.get_chart(self.dbchart.next_chart_id)
        except ResourceError as e:
            return [dict(headers=[], datas=[[], ], name=self.dbchart.title or self.dbchart.name)]

        if self.dbchart.is_drilldown:
            await self.get_filtered_df(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
            for level in range(len(self.index_list)):
                await self.get_index(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD, level=level)
                await self.get_df(fillna=0, ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
                result = self.dh.get_pivot_data_as_raw_data_result()
                headers = await self._get_rawdata_export_headers(result)
                data = await self._get_rawdata_export_datas(result)
                info_list.append(dict(headers=headers, datas=data, name=self.dbchart.title or self.dbchart.name))
        else:
            await self.get_filtered_df(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
            await self.get_index(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
            await self.get_df(fillna=0, ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
            result = self.dh.get_pivot_data_as_raw_data_result()
            headers = await self._get_rawdata_export_headers(result)
            data = await self._get_rawdata_export_datas(result)
            info_list.append(dict(headers=headers, datas=data, name=self.dbchart.title or self.dbchart.name))
        return await self.save_data_to_excel(info_list)

    async def save_data_to_excel(self, info_list):
        chart_name = self.dbchart.title or self.dbchart.name
        chart_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"{chart_name}({chart_time}).xlsx"
        filepath = os.path.join(settings.CHART_EXPORT_PATH, filename)
        dataframe_excel_helper = Dataframe_Excel_Helper()
        dataframe_excel_helper.make_workbook(info_list).save(filepath)
        return filepath

    def _get_series_field(self, series, key_name="field_id"):
        field_id_name = series.get(key_name, "")
        if "\001" in field_id_name:
            field_id, _ = field_id_name.split("\001") # _: colortag_value
            return field_id
        else:
            return field_id_name

    def get_base_chart_option(self):
        if self.dbchart.base_option:
            self.option = json.loads(self.dbchart.base_option)
        else:
            self.option = get_base_chart_option(self.dbchart.ttype)
        return self

    def get_base_series_option(self, ttype=None):
        if ttype:
            option = get_base_series_option(ttype)
        else:
            option = get_base_series_option(self.dbchart.ttype)
        return ObjectDict(option)

    def set_option_x_grid_type(self):
        if self.dbchart.custom_attr is None:
            return self
        if len(self.grid_value_list) == 0:
            return self
        if self.dbchart.custom_attr.get('has_grid', False):
            self.option.grid = double_x_grid
            self.option.xAxis[0].axisLabel.show = False
            self.option.xAxis.append(index_axis(gridIndex=1)())
            self.option.yAxis.append(value_axis(splitNumber=5, gridIndex=1)())
            for dataZoom in self.option.dataZoom:
                dataZoom.xAxisIndex = [0, 1]
        return self

    def set_option_y_grid_type(self):
        if self.dbchart.custom_attr is None:
            return self
        if len(self.grid_value_list) == 0:
            return self
        if self.dbchart.custom_attr.get('has_grid', False):
            self.option.grid = double_y_grid
            self.option.xAxis.append(value_axis(splitNumber=5, gridIndex=1)())
            self.option.yAxis.append(index_axis(gridIndex=1)())
            self.option.yAxis[1].axisLabel.show = False
            for dataZoom in self.option.dataZoom:
                dataZoom.yAxisIndex = [0, 1]
        return self

    async def set_option_radius(self):
        use_pie_loop = self.dbchart.custom_attr.get('use_pie_loop', False)
        pie_loop = self.dbchart.custom_attr.get('pie_loop', ["40%", "80%"])
        if use_pie_loop and pie_loop:
            for _, series in enumerate(self.option.series):
                series.radius = pie_loop
        return self

    async def set_option_axis_line(self):
        length = self.dbchart.custom_attr.get('line_length', 20)
        for i, series in enumerate(self.option.series):
            series.axisLine.lineStyle.width = length
            series.splitLine.length = length
            series.axisTick.length = length // 3
        return self

    async def set_option_axis_label(self):
        show_axis_label = self.dbchart.custom_attr.get('show_axis_label', True)
        if show_axis_label is False:
            for i, series in enumerate(self.option.series):
                series.axisLabel.show = False
        return self

    def hook_visual_map_kwargs(self, visual_map_kwargs):
        visual_map_kwargs.update(dict(dimension=1))

    async def set_option_color(self):
        """
        设置颜色模式, 读取chart.color_type配置
        :return:
        """
        if self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_INDEX:
            await self.set_option_color_set()
        elif self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_VALUE:
            await self.set_option_color_set()
            await self.set_option_value_visualmap_color()
        elif self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_COLORTAG:
            await self.set_option_color_set()
        elif self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_COLOR_VALUE:
            await self.set_option_color_set()
            await self.set_option_color_value_color()
        else:
            await self.set_option_color_set()

    async def set_option_color_set(self):
        if "color_set" in self.dbchart.custom_attr:
            self.option.color = self.dbchart.custom_attr["color_set"]
        else:
            self.option.color = color

    async def set_option_index_color(self):
        for index, series in enumerate(self.option.series):
            series_data_list = []
            for color_index, data_dict in enumerate(series.data):
                data_dict["itemStyle"] = {
                    "normal": {
                        "color": self.option.color[color_index % len(self.option.color)]
                    }
                }
                series_data_list.append(data_dict)
            self.option.series[index].data = series_data_list

    async def set_option_value_color(self):
        pass

    async def set_option_value_visualmap_color(self):
        def _get_text_value(value, base=0):
            return int(value) + base

        for i, series in enumerate(self.option.series):
            field_id = self._get_series_field(series)
            if field_id is None:
                continue
            if not self._has_visual_map(field_id):
                continue
            field = await field_utils.get_field(field_id)
            advanced_color_type = field.custom_attr.get('advanced_color_type', None)
            if (not advanced_color_type) or advanced_color_type == chart_enums.CHART_VMTYPE_NORMAL:
                if field.custom_attr.get('color', None):
                    series.itemStyle.normal.color = field.custom_attr.get('color', None)
            elif advanced_color_type == chart_enums.CHART_VMTYPE_PIECEWISE:
                visual_map = {}
                pieces = field.custom_attr.get('pieces', [])
                out_of_range = field.custom_attr.get('out_of_range', [])
                params = dict(
                    seriesIndex=i,
                    pieces=pieces,
                    padding=0,
                    itemWidth=10,
                    itemHeight=20,
                    outOfRange={
                        "color": out_of_range
                    }
                )
                if self.dbchart.ttype == model_enums.CHART_TTYPE_MAP:
                    params.update(dict(
                        show=True,
                        textGap=1,
                        inverse=False,
                        orient='horizontal',
                    ))
                visual_map = visualmap_piecewise(**params)()

                self.hook_visual_map_kwargs(visual_map)
                self.option.visualMap.append(visual_map)

                series.itemStyle.normal.color = "#909399"
                # series.itemStyle.normal.color = field.custom_attr.get('color', None)
            elif advanced_color_type == chart_enums.CHART_VMTYPE_CONTINUOUS:
                visual_map = {}
                in_range = field.custom_attr.get('inRange', {})
                data_list = self._get_series_data_list(series.data)
                params = dict(
                    seriesIndex=i,
                    min=min(data_list),
                    max=max(data_list),
                    inRange=in_range,
                    padding=0,
                    itemHeight=100,
                    itemWidth=14,
                )
                if self.dbchart.ttype == model_enums.CHART_TTYPE_MAP:
                    params.update(dict(
                        text=[
                            _get_text_value(max(data_list), base=1),
                            _get_text_value(min(data_list), base=-1)
                        ],
                        calculable=False,
                        inverse=False,
                        orient='horizontal',
                    ))
                visual_map = visualmap_continuous(**params)()

                self.hook_visual_map_kwargs(visual_map)
                self.option.visualMap.append(visual_map)

                color_start = in_range.get("color")[0]
                color_end = in_range.get("color")[-1]
                series.itemStyle.normal.color = {
                    "type": 'linear',
                    "x": 0,
                    "y": 0,
                    "x2": 0,
                    "y2": 1,
                    "colorStops": [
                        {
                            "offset": 0, "color": color_start
                        }, 
                        {
                            "offset": 1, "color": color_end
                        }
                    ]
                }

    async def set_option_color_value_color(self):
        # 颜色饱和度
        for color_series in self._color_series_list:
            field_id = color_series["field_id"]
            if field_id is None:
                return None
            field = await field_utils.get_field(field_id)
            color_min = self._get_color_list(field.custom_attr.get('color_min', DEFAULT_MIN_COLOR))
            color_max = self._get_color_list(field.custom_attr.get('color_max', DEFAULT_MAX_COLOR))
            color_series_data_list = self._get_color(color_series["data"], color_min=color_min, color_max=color_max)

            for index in range(len(self.option.series)):
                value_list = self.option.series[index].data

                self.option.series[index].data = []
                for i, (color_value, value) in enumerate(zip(color_series_data_list, value_list)):
                    if isinstance(value, dict):
                        value["itemStyle"] = {
                            "normal": {
                                "color": color_value
                            }
                        }
                        self.option.series[index].data.append(value)
                    else:
                        data = {
                            "value": value,
                            "itemStyle": {
                                "normal": {
                                    "color": color_value
                                }
                            }
                        }
                        self.option.series[index].data.append(data)

    async def set_option_title(self):
        """
        title设置
        显示内容
        是否显示
        :return:
        """
        if self.dbchart.custom_attr.get('show_title', False):
            title_text = self.dbchart.title or self.dbchart.name
            self.option.title.text = self._(title_text)
            self.option.title.show = True
        else:
            self.option.title.show = False

    async def set_option_legend(self, icon="circle"):
        """
        设置 legend
        是否显示
        显示类型
        :param icon:
        :return:
        """
        await self.set_option_legend_show()
        await self.set_option_legend_icon(icon)

    async def set_option_legend_show(self):
        if self.dbchart.custom_attr.get('show_legend', False):
            self.option.legend.show = True
            self.option.grid[0].top = 40
        else:
            self.option.legend.show = False
        return self

    async def set_option_legend_icon(self, icon="circle"):
        icon = self.hook_legend_icon(icon)

        new_data_list = []
        for data in self.legend_data_list:
            if isinstance(data, dict):
                if "icon" in data:
                    new_data_list.append(data)
                elif data.get("pieces", False):
                    data.update({"icon": "path://M 10 10 H 90 V 30 H 10 Z M 10 40 H 90 V 60 H 10 Z M 10 70 H 90 V 90 H 10 Z"})
                    new_data_list.append(data)
                else:
                    data.update({"icon": icon})
                    new_data_list.append(data)
            else:
                new_data_list.append({"name": data, "icon": icon})
        self.option.legend.data = new_data_list
        return self

    async def set_option_smooth(self):
        smooth = self.dbchart.custom_attr.get('line_smooth', False)
        for seires in self.option.series:
            seires.smooth = smooth
        return self

    async def set_option_toolbox(self):
        """
        设置 toolbox
        是否显示
        """
        if self.dbchart.custom_attr.get('show_toolbox', False):
            self.option.toolbox.show = True
        else:
            self.option.toolbox.show = False
        return self

    async def set_option_symbol(self):
        symbol = self.dbchart.custom_attr.get('data_symbol', 'circle')

        if symbol == "invertedTriangle":  # 倒三角
            symbol = INVERTEDTRIANGLE_SVG
        elif symbol == "fork":  # 叉形
            symbol = FORK_SVG
        elif symbol == "plus":  # 加号
            symbol = PLUS_SVG

        for series in self.option.series:
            series.symbol = symbol

        return self

    async def set_option_x_axis(self, data=None, format=False, show_line=True):
        """
        设置 x_axis
        显示名称
        显示轴线
        显示分隔线
        显示标签
        控制是否开始自动转换
        控制是否旋转
        显示数据
        控制显示样式
        :param data: 数据
        :param format: 是否格式化
        :param show_line: 是否显示轴线
        :return:
        """
        await self.set_option_x_axis_title()
        await self.set_option_x_axis_line_hidden(default=show_line)
        await self.set_option_x_axis_splitline_hidden()
        await self.set_option_x_axis_label_hidden()
        await self.set_option_x_axis_auto_change()
        if data is not None:
            await self.set_option_x_axis_data(data)
            # await self.set_option_x_axis_hidden()
            await self.set_option_x_axis_rotate()
        if format:
            await self.set_option_x_axis_formatter()

    async def set_option_x_axis_title(self):
        if self.dbchart.custom_attr.get('showXAxisTitle', False):
            for axis_option in self.option.xAxis:
                axis_option.name = self.dbchart.custom_attr.get('xAxisTitle', "")
                self.option.grid[0].bottom = 14
        else:
            for axis_option in self.option.xAxis:
                axis_option.name = ""
        for axis_option in self.option.xAxis:
            axis_option.nameGap = self.dbchart.custom_attr.get('xAxisNameGap', 22)

    async def set_option_x_axis_data(self, data):
        for axis_option in self.option.xAxis:
            axis_option.data = data

    async def set_option_x_axis_line_hidden(self, default=False):
        if self.dbchart.custom_attr.get('showXAxisLine', default):
            for axis_option in self.option.xAxis:
                axis_option.axisLine.show = True
        else:
            for axis_option in self.option.xAxis:
                axis_option.axisLine.show = False

    async def set_option_x_axis_label_hidden(self):
        if self.dbchart.custom_attr.get('showXAxisLabel', True):
            for axis_option in self.option.xAxis:
                axis_option.axisLabel.show = True
        else:
            for axis_option in self.option.xAxis:
                axis_option.axisLabel.show = False

    async def set_option_x_axis_splitline_hidden(self):
        if self.dbchart.custom_attr.get('showXAxisSplitLine', False):
            for axis_option in self.option.xAxis:
                axis_option.splitLine.show = True
        else:
            for axis_option in self.option.xAxis:
                axis_option.splitLine.show = False

    async def set_option_x_axis_hidden(self):
        for axis_option in self.option.xAxis:
            if axis_option.data == [settings.COLUMN_ALL]:
                axis_option.axisLabel.show = False

    async def set_option_x_axis_rotate(self):
        word_count = _get_word_count('\n'.join(self.option.xAxis[0].data))
        for axis_option in self.option.xAxis:
            if word_count < 170:
                axis_option.axisLabel.rotate = 0
            else:
                axis_option.axisLabel.rotate = -45
        return self

    async def set_option_x_axis_auto_change(self):
        if self.dbchart.custom_attr.get('autoXAxis', False):
            for axis_option in self.option.xAxis:
                axis_option.scale = True

    async def set_option_x_axis_formatter(self):
        formatter_kwargs = self._get_formatter_dict(self.dbchart, key="XAxis_formatter", default_digit=0)
        self.hook_axis_formatter(formatter_kwargs)
        for axis in self.option.xAxis:
            axis.axisLabel.formatter = self._get_formatter_funcstr(**formatter_kwargs)

    async def set_option_y_axis(self, data=None, format=False, show_line=True):
        """
        设置 y_axis
        显示名称
        显示轴线
        显示分隔线
        显示标签
        控制是否开始自动转换
        控制是否旋转
        显示数据
        控制显示样式
        :param data: 数据
        :param format: 是否格式化
        :param show_line: 是否显示轴线
        :return:
        """
        await self.set_option_y_axis_title()
        await self.set_option_y_axis_line_hidden(default=show_line)
        await self.set_option_y_axis_splitline_hidden()
        await self.set_option_y_axis_label_hidden()
        await self.set_option_y_axis_auto_change()
        if data is not None:
            await self.set_option_y_axis_data(data)
            # await self.set_option_y_axis_hidden()
            await self.set_option_y_axis_rotate()
        if format:
            await self.set_option_y_axis_formatter()

    async def set_option_y_axis_title(self):
        if self.dbchart.custom_attr.get('showYAxisTitle', False):
            for axis_option in self.option.yAxis:
                axis_option.name = self.dbchart.custom_attr.get('yAxisTitle', "")
                self.option.grid[0].left = 14
        else:
            for axis_option in self.option.yAxis:
                axis_option.name = ""
        for axis_option in self.option.yAxis:
            axis_option.nameGap = self.dbchart.custom_attr.get('yAxisNameGap', 18)

    async def set_option_y_axis_data(self, data):
        for axis_option in self.option.yAxis:
            axis_option.data = data

    async def set_option_y_axis_line_hidden(self, default=False):
        if self.dbchart.custom_attr.get('showYAxisLine', default):
            for axis_option in self.option.yAxis:
                axis_option.axisLine.show = True
        else:
            for axis_option in self.option.yAxis:
                axis_option.axisLine.show = False

    async def set_option_y_axis_label_hidden(self):
        if self.dbchart.custom_attr.get('showYAxisLabel', True):
            for axis_option in self.option.yAxis:
                axis_option.axisLabel.show = True
        else:
            for axis_option in self.option.yAxis:
                axis_option.axisLabel.show = False

    async def set_option_y_axis_splitline_hidden(self):
        if self.dbchart.custom_attr.get('showYAxisSplitLine', False):
            for axis_option in self.option.yAxis:
                axis_option.splitLine.show = True
        else:
            for axis_option in self.option.yAxis:
                axis_option.splitLine.show = False

    async def set_option_y_axis_hidden(self):
        for axis_option in self.option.yAxis:
            if axis_option.data == [settings.COLUMN_ALL]:
                axis_option.axisLabel.show = False

    async def set_option_y_axis_rotate(self):
        word_count = _get_word_count('\n'.join(self.option.yAxis[0].data))
        for axis_option in self.option.yAxis:
            if word_count < 170:
                axis_option.axisLabel.rotate = 0
            else:
                axis_option.axisLabel.rotate = 45

    async def set_option_y_axis_auto_change(self):
        if self.dbchart.custom_attr.get('autoYAxis', False):
            for axis_option in self.option.yAxis:
                axis_option.scale = True

    async def set_option_y_axis_formatter(self):
        formatter_kwargs = self._get_formatter_dict(self.dbchart, key="YAxis_formatter", default_digit=0)
        self.hook_axis_formatter(formatter_kwargs)
        for axis in self.option.yAxis:
            axis.axisLabel.formatter = self._get_formatter_funcstr(**formatter_kwargs)

    async def set_option_y_sub_axis(self, index=1, data=None, format=False, show_line=True):
        """
        设置 y_axis
        显示名称
        显示轴线
        显示分隔线
        显示标签
        控制是否开始自动转换
        控制是否旋转
        显示数据
        控制显示样式
        :param index: 第几根y轴， 默认1， 指代第二y轴， 第一个从轴
        :param data: 数据
        :param format: 是否格式化
        :param show_line: 是否显示轴线
        :return:
        """
        await self.set_option_y_sub_axis_title(index=index)
        await self.set_option_y_sub_axis_line_hidden(index=index, default=show_line)
        await self.set_option_y_sub_axis_splitline_hidden(index=index)
        await self.set_option_y_sub_axis_label_hidden(index=index)
        await self.set_option_y_sub_axis_auto_change(index=index)
        if data is not None:
            await self.set_option_y_sub_axis_data(data, index=index)
            await self.set_option_y_sub_axis_rotate(index=index)
        if format:
            await self.set_option_y_sub_axis_formatter(index=index)

    async def set_option_y_sub_axis_title(self, index=1):
        if self.dbchart.custom_attr.get('showYSubAxisTitle', False):
            self.option.yAxis[index].name = self.dbchart.custom_attr.get('ySubAxisTitle', "")
            self.option.grid[0].right = 14
        else:
            self.option.yAxis[index].name = ""
        self.option.yAxis[index].nameGap = self.dbchart.custom_attr.get('ySubAxisNameGap', 20)

    async def set_option_y_sub_axis_data(self, data, index=1):
        self.option.yAxis[index].data = data

    async def set_option_y_sub_axis_line_hidden(self, index=1, default=False):
        if self.dbchart.custom_attr.get('showYSubAxisLine', default):
            self.option.yAxis[index].axisLine.show = True
        else:
            self.option.yAxis[index].axisLine.show = False

    async def set_option_y_sub_axis_label_hidden(self, index=1):
        if self.dbchart.custom_attr.get('showYSubAxisLabel', True):
            self.option.yAxis[index].axisLabel.show = True
        else:
            self.option.yAxis[index].axisLabel.show = False

    async def set_option_y_sub_axis_splitline_hidden(self, index=1):
        if self.dbchart.custom_attr.get('showYSubAxisSplitLine', False):
            self.option.yAxis[index].splitLine.show = True
        else:
            self.option.yAxis[index].splitLine.show = False

    async def set_option_y_sub_axis_hidden(self):
        for axis_option in self.option.yAxis:
            if axis_option.data == [settings.COLUMN_ALL]:
                axis_option.axisLabel.show = False

    async def set_option_y_sub_axis_rotate(self, index=1):
        word_count = _get_word_count('\n'.join(self.option.yAxis[1].data))
        if word_count < 170:
            self.option.yAxis[index].axisLabel.rotate = 0
        else:
            self.option.yAxis[index].axisLabel.rotate = 45

    async def set_option_y_sub_axis_auto_change(self, index=1):
        if self.dbchart.custom_attr.get('autoYSubAxis', False):
            self.option.yAxis[index].scale = True

    async def set_option_y_sub_axis_formatter(self, index=1):
        formatter_kwargs = self._get_formatter_dict(self.dbchart, key="YSubAxis_formatter", default_digit=0)
        self.hook_axis_formatter(formatter_kwargs)
        self.option.yAxis[index].axisLabel.formatter = self._get_formatter_funcstr(**formatter_kwargs)

    def hook_data_zoom(self):
        data_zoom_settings = self.dbchart.custom_attr.get('datazoom', [])
        for dataZoom, dz_settings in zip(self.option.dataZoom, data_zoom_settings):
            if dz_settings is not None:
                dataZoom.start = dz_settings.get('start')
                dataZoom.end = dz_settings.get('end')

    async def set_option_data_zoom(self, multi_color_tag=True):
        """
        设置 datazoom
        控制显示
        控制起始值
        :param multi_color_tag:
        :return:
        """
        if len(self.option.series) == 0:
            return self

        if len(self.grid_value_list) > 0:
            coefficient = 1 - 1.0 * len(self.grid_value_list) / len(self.option.series)
        else:
            coefficient = 1

        if self.dbchart.custom_attr.get("show_datazoom", False):
            for dataZoom in self.option.dataZoom:
                dataZoom.show = True

        if multi_color_tag and self._has_color_tag():
            length = len(self.option.series) * len(self.option.series[0]["data"]) * coefficient
            if length <= 20:
                return self
        else:
            length = len(self.option.series[0]["data"]) * coefficient
            if length <= 20:
                return self

        for dataZoom in self.option.dataZoom:
            dataZoom.show = True
            dataZoom.start = math.ceil(100 - 20.0 / length * 100)
            dataZoom.end = 100

        self.hook_data_zoom()
        return self

    def _get_formatter_dict(self, obj, key="default_field_formatter", default_digit=2, default_show_text=False, default_show_value=True):
        formatter_dict = dict()
        formatter_dict["showText"] = self.dbchart.custom_attr.get("formatter", {}).get("showText", default_show_text)
        formatter_dict["showValue"] = self.dbchart.custom_attr.get("formatter", {}).get("showValue", default_show_value)
        formatter_dict["showPercent"] = self.dbchart.custom_attr.get("formatter", {}).get("showPercent", True)
        formatter_dict["percentDigit"] = self.dbchart.custom_attr.get("formatter", {}).get("percentDigit", 1)
        if key in obj.custom_attr and obj.custom_attr[key]:
            formatter_dict["ttype"] = ttype = obj.custom_attr[key].get('type', "num")
            if ttype in obj.custom_attr[key]:
                formatter_dict["digit"] = obj.custom_attr[key][ttype].get('digit', default_digit)
                formatter_dict["unit"] = obj.custom_attr[key][ttype].get('unit', '')
                formatter_dict["millesimal"] = obj.custom_attr[key][ttype].get('millesimal', False)
        else:
            formatter_dict["ttype"] = "num"
            formatter_dict["digit"] = default_digit
            formatter_dict["unit"] = ''
            formatter_dict["millesimal"] = False
        return formatter_dict

    def _get_formatter_funcstr(self, default_digit=2, default_show_text=False, default_show_value=True, **kwargs):
        return "\
$$this.getNormalFormatterHandler({{\
ttype: '{ttype}', \
digit: {digit}, \
unit: '{unit}', \
millesimal: {millesimal}, \
showText: {showText}, \
showValue: {showValue}, \
showPercent: {showPercent}, \
percentDigit: {percentDigit}, \
usage: '{usage}'\
}})$$".format(
            ttype=kwargs.get("ttype", "num"),
            digit=kwargs.get("digit", default_digit),
            unit=kwargs.get("unit", ''),
            percentDigit=kwargs.get("percentDigit", 1),
            millesimal=consts.TEXT_BOOLEAN[kwargs.get("millesimal", False)],
            showText=consts.TEXT_BOOLEAN[kwargs.get("showText", default_show_text)],
            showValue=consts.TEXT_BOOLEAN[kwargs.get("showValue", default_show_value)],
            showPercent=consts.TEXT_BOOLEAN[kwargs.get("showPercent", True)],
            usage=kwargs.get("usage", None),
        )

    def _get_formatter_lastdict(self, default_digit=2, **kwargs):
        return {
            "ttype": kwargs.get("ttype", "num"),
            "digit": kwargs.get("digit", default_digit),
            "unit": kwargs.get("unit", ''),
            "millesimal": kwargs.get("millesimal", False),
            "showText": kwargs.get("showText", False),
            "showValue": kwargs.get("showValue", True),
            "showPercent": kwargs.get("showPercent", True),
            "percentDigit": kwargs.get("percentDigit", 1),
            "usage": kwargs.get("usage", None),
        }

    def hook_axis_formatter(self, formatter_kwargs):
        formatter_kwargs.update(
            dict(
                showText=False,
                showValue=True,
                showPercent=True,
                usage="axis",
            )
        )

    def hook_label_formatter(self, formatter_kwargs):
        formatter_kwargs.update(
            dict(
                usage="label",
            )
        )

    def hook_tooltip_formatter(self, formatter_kwargs):
        formatter_kwargs.update(
            dict(
                usage="tooltip",
            )
        )

    def hook_formatter_dict_formatter(self, formatter_kwargs):
        formatter_kwargs.update(
            dict(
                usage="formatter_dict",
            )
        )

    def hook_legend_icon(self, icon="circle"):
        return icon

    async def set_option_series_formatter(self):
        """
        设置显示样式
        :return:
        """
        for series in self.option.series:
            if self._has_color_tag():
                field_id = self._get_series_field(series)
                if field_id is None:
                    if len(self.value_list) == 1:
                        field = self.value_list[0]
                    else:
                        continue
                else:
                    field = await field_utils.get_field(field_id)
            else:
                field_id = self._get_series_field(series)
                if field_id is None:
                    continue
                field = await field_utils.get_field(field_id)

            formatter_kwargs = self._get_formatter_dict(field, key="default_field_formatter")

            self.hook_label_formatter(formatter_kwargs)
            series.label.normal.formatter = self._get_formatter_funcstr(**formatter_kwargs)

            self.hook_tooltip_formatter(formatter_kwargs)
            series.tooltip.formatter = self._get_formatter_funcstr(**formatter_kwargs)

            self.hook_formatter_dict_formatter(formatter_kwargs)
            self.formatterDict[series.name] = self._get_formatter_lastdict(**formatter_kwargs)

        if self.dbchart.ttype in (
                model_enums.CHART_TTYPE_BAR_STACK,
                model_enums.CHART_TTYPE_BAR_STACK_PERCENT,
                model_enums.CHART_TTYPE_HBAR_STACK,
                model_enums.CHART_TTYPE_HBAR_STACK_PERCENT,
                model_enums.CHART_TTYPE_BARLINE,
                model_enums.CHART_TTYPE_BARLINE_STACK,
                model_enums.CHART_TTYPE_LINE,
                model_enums.CHART_TTYPE_LINE_SHADOW,
                model_enums.CHART_TTYPE_LINE_STACK,
        ):
            self.option.tooltip.formatter = "$$this.getGlobalFormatterHandler$$"

    def _get_color_tag_mark_line_data(self, line_type, field_id):
        result = self.dh.get_pivot_data_result()
        all_result_data_list = []
        for data in result['data']:
            all_result_data_list.extend([v if v != settings.NONE_DATA else 0 for v in data['value']])
        if line_type == 'min':
            return min(all_result_data_list)
        elif line_type == 'max':
            return max(all_result_data_list)
        elif line_type == 'average':
            return sum(all_result_data_list) / len(all_result_data_list)

    async def _get_calc_mark_line_data(self, field_id):
        if field_id is None:
            return None
        field = await field_utils.get_field(field_id)
        column = await column_utils.get_column(field.column_id)
        pivot = Pivot_main(field_id, [settings.COLUMN_ALL], column.aggable, field.get_func(), field.multifunc, field.sortfunc, field.sort_regiontype_id)
        series = self.dh._get_serie_data(pivot)  # 这里每种类型数据源应该要不一样
        return float(series.values[0])

    async def _get_series_index(self, field_id, type_line_data):
        if field_id is None:
            return -1, type_line_data
        field_name = await self._convert_field_name(field_id)  # 指定要为哪个字段设置mark_line
        for index, series in enumerate(self.option.series):
            if series.name == field_name:
                return index, type_line_data
        else:
            return -1, type_line_data

    async def set_option_mark_line(self):
        """
        控制辅助线
        :return:
        """
        if self.dbchart.custom_attr.get('mark_line', False):
            for x in self.dbchart.markline:
                line_field_id = x.get('field')
                line_type = x.get('type')

                type_line_data = {
                    'name': x.get('name'),
                    'axis': None,
                    'lineStyle': {
                        'normal': {
                            'type': x.get('line_type'),
                            'width': x.get('line_width', 1),
                            'color': x.get('color')
                        }
                    }
                }

                if line_type == 'custom':
                    type_line_data.update(
                        dict(
                            axis=x.get('data'),
                        )
                    )
                elif line_type == 'calc':
                    type_line_data.update(
                        dict(
                            axis=await self._get_calc_mark_line_data(x.get('field_id')),
                        )
                    )
                elif self._has_color_tag():
                    type_line_data.update(
                        dict(
                            axis=self._get_color_tag_mark_line_data(line_type, line_field_id),
                        )
                    )
                else:
                    type_line_data.update(
                        dict(
                            type=line_type,
                        )
                    )

                (index, type_line_data) = await self._get_series_index(line_field_id, type_line_data)
                if not ~index and len(self.option.series) > 0:
                    self.option.series[0].markLine.data.append(type_line_data)
                else:
                    self.option.series[index].markLine.data.append(type_line_data)

        return self
