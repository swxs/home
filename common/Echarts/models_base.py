# coding=utf8

import math
import json
import datetime
import numpy as np
import pandas as pd
from tornado.util import ObjectDict

try:
    Period = pd.Period
except AttributeError:
    Period = pd._libs.period.Period

import settings
from api.consts import const
from api.consts.bi import field as field_consts
from api.consts.bi import chart as chart_consts
from api.utils.bi.field import Field
from common.Exceptions import NoDataException
from common.Echarts.option_chart import (
    get_base_chart_option,
    double_x_grid,
    double_y_grid,
    index_axis,
    value_axis,
    visualmap_piecewise,
    visualmap_continuous
)
from common.Echarts.option_serie import get_base_serie_option
from common.DHelper import DHelper_factory
from common.DHelper.DHelper_base import Pivot_main
from common.Utils.translation import get_translate_and_code
from common.Utils.validate import Validate, RegType
from common.Utils.log_utils import getLogger

log = getLogger("echarts")


class Vtype:
    N_VALUE_N_COLOR_N_INDEX = 0  # 不出图
    N_VALUE_N_COLOR_Y_INDEX = 1  # 不出图
    N_VALUE_Y_COLOR_N_INDEX = 2  # 不出图
    N_VALUE_Y_COLOR_Y_INDEX = 3  # 不出图
    Y_VALUE_N_COLOR_N_INDEX = 4  # 1栏 全体数据处理             [度量]
    Y_VALUE_N_COLOR_Y_INDEX = 5  # n栏 全体数据处理             [度量]
    Y_VALUE_Y_COLOR_N_INDEX = 6  # 1栏 全体数据根据对比拆分1个度量 [对比]
    Y_VALUE_Y_COLOR_Y_INDEX = 7  # n栏 全体数据根据对比拆分1个度量 [对比]


class BaseChart(object):
    def __init__(self, dbchart, **params):
        self.dbchart = dbchart
        self.params = params
        self.realtime_filter = params.get('realtime_filter', dict())
        if not self.realtime_filter.get("data_filter_list"):
            self.realtime_filter["data_filter_list"] = []
        if not self.realtime_filter.get("drilldown_list"):
            self.realtime_filter["drilldown_list"] = []
        self.custom_attr = self.realtime_filter.get('custom_attr', dict())
        self.value_field_id_list = self.realtime_filter.get('value_field_id_list', [])
        self.region_id_list = params.get('region_id_list', [])
        self.locale = self.params.get('locale', None)
        self._, self.code = get_translate_and_code(self.locale)
        self.dh = DHelper_factory.get_dhelper(self.dbchart.worktable)

        self.index_list = self.dbchart.index_field_list
        self.value_list = self.dbchart.value_field_list
        if self.value_field_id_list:
            self.value_list += [Field.get_field_by_field_id(field_id) for field_id in self.value_field_id_list]
        self.sub_value_list = self.dbchart.sub_value_field_list
        self.grid_value_list = self.dbchart.grid_value_field_list
        self.color_value_list = self.dbchart.color_value_field_list
        self.colortag = self.dbchart.colortag_field
        self.tag_value_list = self.dbchart.tag_value_field_list
        self.convert_table = self.dbchart.convert_table
        self.vtype = self._get_vtype()
        self.formatterDict = dict()

    def _has_value(self):
        return (self.vtype & 4) > 0

    def _has_color(self):
        return (self.vtype & 2) > 0

    def _has_index(self):
        return (self.vtype & 1) > 0

    def _has_colortag(self):
        return self.colortag is not None

    def _has_visualmap(self, field_id):
        if self.colortag is not None:
            return False
        for field in self.value_list:
            if field_id == field.id:
                return True
        for field in self.grid_value_list:
            if field_id == field.id:
                return True
        return False

    def _is_index(self, field_id):
        if field_id is None:
            return False
        if Validate.check(field_id, reg_type=RegType.COLUMN_ID):
            field = Field.get_field_by_field_id(field_id)
            if field.dim_measure == field_consts.STYPE_INDEX:
                return True
        return False

    def _convert_field_name(self, field_id):
        """
        将field_id转换成对应的名字
        :param field_id:
        :return:
        """
        if (Validate.check(field_id, reg_type=RegType.COLUMN_ID)) and ((field_id in self.dbchart.field_id_list) or (field_id in self.value_field_id_list)):
            field = Field.get_field_by_field_id(field_id)
            return self._(field.display_name)
        else:
            return self._convert_colortag_name(field_id)

    def _convert_colortag_name(self, column):
        """
        将colortag的值转换成对应的映射值
        :param column:
        :return:
        """
        if self.colortag is not None:
            if self.colortag.column in self.convert_table:
                try:
                    return self._(self.convert_table[self.colortag.column][int(float(column))])
                except:
                    return column
            return column
        else:
            return column

    def _convert_column_name(self, index, field_id=None, field_list=None):
        """
        将维度值转换成映射的文字
        :param index:
        :param field_id:
        :param field_list:
        :return:
        """
        if field_list and len(field_list) == 1:
            field_id = field_list[0]
        if self._is_index(field_id):
            field = Field.get_field_by_field_id(field_id)
            if field.column.col in self.convert_table:
                if math.isnan(index):
                    return settings.NONE_DATA
                elif np.isinf(index):
                    return settings.NONE_DATA  # 这里原本返回"Inf"， 在echart中没有正常的表现， 现在暂时使用"N/A"
                else:
                    if int(float(index)) in self.convert_table[field.column.col]:
                        return self._(self.convert_table[field.column.col][int(float(index))])
                    else:
                        log.error(f"field: {field.id} has no option {int(float(index))}")
                        return settings.NONE_DATA
        if isinstance(index, (tuple, list)):
            changed_index_list = [self._convert_column_name(x, field_id=field_list[i]) for i, x in enumerate(index)]
            key = reversed(changed_index_list)
            name = '\n'.join(key)
            return name
        else:
            return self._convert_name(index)

    def _convert_column_name_origin(self, index, field_id=None, field_list=None):
        if field_list and len(field_list) == 1:
            field_id = field_list[0]
        if self._is_index(field_id):
            field = Field.get_field_by_field_id(field_id)
            if field.column in self.convert_table:
                if math.isnan(index):
                    return {const.BASE_LOCALE: settings.NONE_DATA, self.code: settings.NONE_DATA}
                elif np.isinf(index):
                    return {const.BASE_LOCALE: settings.NONE_DATA,
                            self.code: settings.NONE_DATA}  # 这里原本返回"Inf"， 在echart中没有正常的表现， 现在暂时使用"N/A"
                else:
                    value = self.convert_table[field.column.col][int(float(index))]
                    return {const.BASE_LOCALE: value, self.code: self._(value)}
        if isinstance(index, tuple):
            changed_index_list = [self._convert_column_name_origin(x, field_id=field_list[i]) for i, x in enumerate(index)]
            base_changed_index_list = [x.get(const.BASE_LOCALE) for x in changed_index_list]
            base_key = reversed(base_changed_index_list)
            base_name = '\n'.join(base_key)
            code_changed_index_list = [x.get(self.code) for x in changed_index_list]
            code_key = reversed(code_changed_index_list)
            code_name = '\n'.join(code_key)
            return {const.BASE_LOCALE: base_name, self.code: code_name}
        else:
            value = self._convert_name(index)
            return {const.BASE_LOCALE: value, self.code: self._(value)}

    def _convert_name(self, index):
        """
        将值处理成字符串
        :param index:
        :return:
        """
        if isinstance(index, (tuple, list)):
            changed_index_list = [self._convert_name(x) for x in index]
            key = reversed(changed_index_list)
            name = '\n'.join(key)
        elif isinstance(index, (np.int, np.int8, np.int16, np.int32, np.int64)):
            name = index
        elif isinstance(index, (np.float, np.float16, np.float32, np.float64)):
            if math.isnan(index):
                name = settings.NONE_DATA
            elif np.isinf(index):
                name = settings.NONE_DATA
            else:
                name = index.replace("nan", settings.NONE_DATA)
        elif isinstance(index, datetime.datetime):
            if isinstance(index, pd._libs.tslib.NaTType):
                name = settings.NONE_DATA
            else:
                name = index.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(index, datetime.date):
            if isinstance(index, pd._libs.tslib.NaTType):
                name = settings.NONE_DATA
            else:
                name = index.strftime('%Y-%m-%d 00:00:00')
        else:
            try:
                name = index
            except:
                index, type(index)
                name = index
        return name

    def _clear_data(self, value):
        if isinstance(value, (np.float, np.float16, np.float32, np.float64)):
            if math.isnan(value):
                value = settings.NONE_DATA
            elif np.isinf(value):
                value = settings.NONE_DATA
        return value

    def _get_drilldown_info(self):
        if self.dbchart.is_drilldown and hasattr(self, 'drilldown_field_id'):
            self.drilldown_info = [self._convert_column_name_origin(value, field_id=self.drilldown_field_id) for value
                                   in self.dh.get_field_unique_value_list(self.drilldown_field_id)]
        else:
            self.drilldown_info = []
        return self.drilldown_info

    def _get_color_list(self, color):
        if color is None:
            return None
        else:
            return [int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)]

    def _get_series_data_list(self, data_list):
        return [data if not isinstance(data, dict) else data.get('value') for data in data_list]

    def _get_color(self, data_list, color_min=None, color_max=None):
        if color_min is None:
            color_min = self._get_color_list("#bce4d8")
        if color_max is None:
            color_max = self._get_color_list("#2c5985")
        color_list = []
        tmp_data_list = [data if data not in ["-", float("inf"), float("-inf")] else 0 for data in data_list]
        if tmp_data_list:
            min_data, max_data = min(tmp_data_list), max(tmp_data_list)
            for data in tmp_data_list:
                if max_data - min_data == 0:
                    color_0 = (color_min[0] + color_max[0]) // 2
                    color_1 = (color_min[1] + color_max[1]) // 2
                    color_2 = (color_min[2] + color_max[2]) // 2
                else:
                    color_0 = int((data * color_max[0] - data * color_min[0] + max_data * color_min[0] - min_data *
                                   color_max[0]) / (max_data - min_data))
                    color_1 = int((data * color_max[1] - data * color_min[1] + max_data * color_min[1] - min_data *
                                   color_max[1]) / (max_data - min_data))
                    color_2 = int((data * color_max[2] - data * color_min[2] + max_data * color_min[2] - min_data *
                                   color_max[2]) / (max_data - min_data))
                color_list.append("#{0}{1}{2}".format(hex(color_0)[2:4], hex(color_1)[2:4], hex(color_2)[2:4]))
        return color_list

    def get_filtered_df(self, ttype=chart_consts.CHART_SHOW):
        self.dbchart.get_changed_df(realtime_filter=self.realtime_filter, region_id_list=self.region_id_list, ttype=ttype)
        self.dh.do_preprocess()

    @classmethod
    def delete_df_already_used_column(self, func):
        def inner(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.dh.do_refresh(self.dbchart.field_id_list)
            return result

        return inner

    def _get_vtype(self):
        # 计算类型
        vtype = 0
        if len(self.value_list) != 0 or len(self.value_field_id_list) != 0:
            vtype += 4
        if self.colortag is not None:
            vtype += 2
        if len(self.index_list) != 0:
            vtype += 1
        return vtype

    def get_index(self, ttype=chart_consts.CHART_SHOW, level=None):
        if ttype == chart_consts.CHART_SHOW and self.dbchart.is_drilldown:
            self.drilldown_level = len(self.realtime_filter["drilldown_list"])
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
            self.sub_index = ['All']
        if len(self.main_index) == 0:
            self.main_index = ["All"]
        return self.main_index, self.sub_index

    def _convert_field_to_main_pivot(self, field):
        return field.id, self.main_index, field.aggable, field.get_func(), field.multifunc, field.sortfunc, field.sort_regiontype_id

    def _convert_field_to_sub_pivot(self, field):
        return field.id, self.sub_index, field.aggable, field.get_func(), field.multifunc, field.sortfunc, field.sort_regiontype_id

    def get_df(self, fillna=settings.NONE_DATA, ttype=chart_consts.CHART_SHOW):
        for field in self.value_list:
            self.dh.add_main_pivot(*self._convert_field_to_main_pivot(field))

        for field in self.sub_value_list:
            self.dh.add_sub_pivot(*self._convert_field_to_sub_pivot(field))

        if self.dbchart.custom_attr and self.dbchart.custom_attr.get('has_grid', False):
            for field in self.grid_value_list:
                self.dh.add_sub_pivot(*self._convert_field_to_sub_pivot(field))

        if ttype != chart_consts.CHART_DOWNLOAD:
            if len(self.color_value_list) > 0:
                self.dh.add_sub_pivot(*self._convert_field_to_sub_pivot(self.color_value_list[0]))

            for field in self.tag_value_list:
                self.dh.add_sub_pivot(*self._convert_field_to_sub_pivot(field))
        self.dh.do_pivot(self._has_colortag(), fillna=fillna)

    def get_ranked_df(self):
        if self.dbchart.custom_attr is not None and self.dbchart.custom_attr.get("showChartSort", False):
            if self.vtype in [Vtype.Y_VALUE_N_COLOR_Y_INDEX, Vtype.Y_VALUE_Y_COLOR_Y_INDEX]:
                dtype = 1
            elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_Y_COLOR_N_INDEX]:
                dtype = 2
            else:
                dtype = 0

            if self.dbchart.custom_attr.get("sortType", "desc") == "asc":
                ascending = True
            else:
                ascending = False

            sortIndex = self.dbchart.custom_attr.get("sortIndex", 0)

            if self.dbchart.custom_attr.get("xAxisLimit", False):
                xAxisCount = self.dbchart.custom_attr.get("xAxisCount", None)
            else:
                xAxisCount = None

            self.dh.do_rank(dtype, ascending, sortIndex, xAxisCount)

    def get_pivot_df(self):
        if not self._has_value():
            return False
        else:
            self.get_df()
            return True

    def get_series_list(self):
        series_list = []
        result = self.dh.get_pivot_data_result()
        self.axis_data_list = [self._convert_column_name(x, field_list=result["head"]["name"]) for x in result["head"]["value"]]
        self.legend_data_list = []
        for data in result["data"]:
            index_name = self._convert_field_name(data["name"])
            if data["name"] in [x.id for x in self.sub_value_list]:
                field = Field.get_field_by_field_id(data["name"])
                series_option = self.get_base_series_option(ttype=field.ttype)
                if field.custom_attr.get('color', None):
                    series_option.itemStyle.normal.color = field.custom_attr.get('color', None)
                self.legend_data_list.append({"name": index_name, "icon": "line"})
            elif data["name"] in [x.id for x in self.grid_value_list]:
                field = Field.get_field_by_field_id(data["name"])
                series_option = self.get_base_series_option(ttype=field.ttype)
                if field.custom_attr.get('color', None):
                    series_option.itemStyle.normal.color = field.custom_attr.get('color', None)
                series_option.xAxisIndex = len(self.option.xAxis) - 1
                series_option.yAxisIndex = len(self.option.yAxis) - 1
            elif data["name"] in [x.id for x in self.tag_value_list]:
                field = Field.get_field_by_field_id(data["name"])
                series_option = self.get_base_series_option(ttype=field.ttype)
            else:
                series_option = self.get_base_series_option()
                self.legend_data_list.append(index_name)
                if self.colortag is None:
                    field = Field.get_field_by_field_id(data["name"])
                    if field.custom_attr.get('color', None):
                        series_option.itemStyle.normal.color = field.custom_attr.get('color', None)

            if series_option:
                series_option.data = [self._clear_data(value) for value in data["value"]]
                series_option.field_id = data["name"]
                series_option.id = data["name"]
                series_option.name = index_name
                series_list.append(series_option)
        self.option.series = series_list

    def change_series_percent(self, fillna="-"):
        data_all = []
        if len(self.option.series) == 0:
            raise NoDataException
        for i in range(len(self.option.series[0].data)):
            data_all.append(0)
        for series in self.option.series:
            for i, data in enumerate(series.data):
                if data != fillna:
                    data_all[i] += data
        for series in self.option.series:
            for i, data in enumerate(series.data):
                if data != fillna:
                    series.data[i] = data / float(data_all[i]) * 100
                else:
                    series.data[i] = fillna

    def to_option(self):
        raise Exception('should be implimented in sub class')

    def _get_rawdata_export_headers(self, result):
        return [self._convert_field_name(x) for x in result["head"]["value"]]

    def _get_rawdata_export_datas(self, result):
        return [[self._convert_column_name(value, field_id=result["head"]["value"][i])
                 for i, value in enumerate(data["value"])]
                for data in result["data"]]

    def to_base_data(self):
        base_data = self.dh.get_base_data()
        return base_data

    def to_export_data(self):
        info_list = list()
        try:
            if self.dbchart.next_chart is not None:
                old_value_list = self.value_list
                self.realtime_filter['value_field_id_list'] = self.value_field_id_list = [field.id for field in old_value_list]
                self.dbchart = self.dbchart.get_chart_by_chart_id(self.dbchart.next_chart)
                self.index_list = self.dbchart.get_index_list_as_json()
                self.value_list = self.dbchart.get_value_list_as_json()
                if self.value_field_id_list:
                    self.value_list += [Field.get_field_by_field_id(field_id).to_front() for field_id in self.value_field_id_list]
                self.sub_value_list = self.dbchart.get_sub_value_list_as_json()
                self.grid_value_list = self.dbchart.get_grid_value_list_as_json()
                self.color_value_list = self.dbchart.get_color_value_field_as_json()
                self.colortag = self.dbchart.get_colortag_field_as_json()
                self.tag_value_list = self.dbchart.get_tag_value_list_as_json()
                self.convert_table = self.dbchart.convert_table
                self.vtype = self._get_vtype()
            self.get_filtered_df(ttype=chart_consts.CHART_DOWNLOAD)
        except NoDataException:
            return [dict(headers=[], datas=[[], ], name=self.dbchart.name)]

        if self.dbchart.is_drilldown:
            for level in range(len(self.index_list)):
                self.get_index(ttype=chart_consts.CHART_DOWNLOAD, level=level)
                self.get_df(fillna=0, ttype=chart_consts.CHART_DOWNLOAD)
                result = self.dh.get_pivot_data_as_raw_data_result()
                headers = self._get_rawdata_export_headers(result)
                datas = self._get_rawdata_export_datas(result)
                info_list.append(dict(headers=headers, datas=datas, name=self.dbchart.name))
        else:
            self.get_index(ttype=chart_consts.CHART_DOWNLOAD)
            self.get_df(fillna=0, ttype=chart_consts.CHART_DOWNLOAD)
            result = self.dh.get_pivot_data_as_raw_data_result()
            headers = self._get_rawdata_export_headers(result)
            datas = self._get_rawdata_export_datas(result)
            info_list.append(dict(headers=headers, datas=datas, name=self.dbchart.name))
        return info_list

    def get_base_chart_option(self):
        if self.dbchart.base_option:
            option = json.loads(self.dbchart.base_option)
        else:
            option = get_base_chart_option(self.dbchart.ttype)
        self.option = ObjectDict(option)
        return self

    def get_base_series_option(self, ttype=None):
        if ttype:
            option = get_base_serie_option(ttype)
        else:
            option = get_base_serie_option(self.dbchart.ttype)
        return ObjectDict(option)

    def set_option_x_grid_type(self):
        if self.dbchart.custom_attr is None:
            return self
        if len(self.grid_value_list) == 0:
            return self
        if self.dbchart.custom_attr.get('has_grid', False):
            self.option.grid = double_x_grid
            self.option.xAxis[0].axisLabel.show = False
            self.option.xAxis.append(index_axis().clone(gridIndex=1))
            self.option.yAxis.append(value_axis().clone(splitNumber=2, gridIndex=1))
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
            self.option.xAxis.append(value_axis().clone(splitNumber=2, gridIndex=1))
            self.option.yAxis.append(index_axis().clone(gridIndex=1))
            self.option.yAxis[1].axisLabel.show = False
            for dataZoom in self.option.dataZoom:
                dataZoom.yAxisIndex = [0, 1]
        return self

    def set_option_radius(self):
        min = 20.0
        max = 80.0
        if len(self.option.series) > 1:
            per_radius = (max - min) / (3 * len(self.option.series) - 1)
            for i, serie in enumerate(self.option.series):
                inner_radius = min + 3 * i * per_radius
                serie.radius = ["{0}%".format(inner_radius), "{0}%".format(inner_radius + 2.5 * per_radius)]
                serie.z = serie.z + len(self.option.series) - i
        return self

    def set_option_visualmap(self):
        def _get_text_value(value, base=0):
            return int(value) + base

        for i, series in enumerate(self.option.series):
            field_id = series.get('field_id')
            if not self._has_visualmap(field_id):
                continue
            field = Field.get_field_by_field_id(field_id)
            if field.custom_attr and field.custom_attr.get('advanced_color', False):
                advanced_color_type = field.custom_attr.get('advanced_color_type', None)
                if advanced_color_type == field_consts.VMTYPE_PIECEWISE:
                    pieces = field.custom_attr.get('pieces', [])
                    parmas = dict(
                        seriesIndex=i,
                        pieces=pieces,
                        padding=0,
                        itemWidth=10,
                        itemHeight=20,
                    )
                    if self.dbchart.ttype == chart_consts.CHART_TYPE_MAP:
                        parmas.update(dict(
                            show=True,
                            textGap=1,
                            inverse=False,
                            orient='horizontal',
                        ))
                    visualmap = visualmap_piecewise().clone(**parmas)
                elif advanced_color_type == field_consts.VMTYPE_CONTINUOUS:
                    inRange = field.custom_attr.get('inRange', {})
                    data_list = self._get_series_data_list(series.data)
                    parmas = dict(
                        show=True,
                        seriesIndex=i,
                        min=min(data_list),
                        max=max(data_list),
                        inRange=inRange,
                        padding=0,
                        itemHeight=100,
                        itemWidth=14,
                    )
                    if self.dbchart.ttype == chart_consts.CHART_TYPE_MAP:
                        parmas.update(dict(
                            text=[_get_text_value(max(data_list), base=1), _get_text_value(min(data_list), base=-1)],
                            calculable=False,
                            inverse=False,
                            orient='horizontal',
                        ))
                    visualmap = visualmap_continuous().clone(**parmas)
                else:
                    visualmap = {}

                if 'hbar' in self.dbchart.ttype or self.dbchart.ttype == chart_consts.CHART_TYPE_MAP:
                    visualmap["dimension"] = 0
                else:
                    visualmap["dimension"] = 1

                if visualmap:
                    self.option.visualMap.append(visualmap)
        return self

    def set_option_colorset(self):
        if len(self.color_value_list) > 0:
            self.option.legend.data.pop(-1)
            series = self.option.series.pop(-1)
            field = Field.get_field_by_field_id(series.field_id)
            color_min = self._get_color_list(field.custom_attr.get('color_min', "#bce4d8"))
            color_max = self._get_color_list(field.custom_attr.get('color_max', "#2c5985"))
            color_value_list = self._get_color(series.data, color_min=color_min, color_max=color_max)
            old_color_list = self.option.series[0].data
            self.option.series[0].data = []
            for i, color_value in enumerate(color_value_list):
                data_map = {
                    "value": old_color_list[i],
                    "itemStyle": {
                        "normal": {
                            "color": color_value_list[i]
                        }
                    }
                }
                self.option.series[0].data.append(data_map)
        return self

    def set_color(self):
        self.option.color = ["#577CAD", "#FFA51B", "#EF635C", "#7FBAC4", "#48A47D", "#BCB52B", "#B46A88", "#B29688", "#9FACA4", "#6B6B6B", ]
        return self

    def set_option_legend_icon(self, ttype="circle"):
        self.option.legend.data = [x if isinstance(x, dict) else {"name": x, "icon": ttype} for x in self.legend_data_list]
        return self

    def set_option_title(self):
        if self.dbchart.custom_attr_objectdict.show_title:
            title_text = self.dbchart.title or self.dbchart.name
            self.option.title.text = self._(title_text)
            self.option.title.show = True
        else:
            self.option.title.show = False
        return self

    def set_option_legend(self):
        if self.dbchart.custom_attr_objectdict.show_legend:
            self.option.legend.show = True
        else:
            self.option.legend.show = False
        return self

    def set_option_smooth(self):
        smooth = self.dbchart.custom_attr.get('line_smooth', False)
        for seires in self.option.series:
            seires.smooth = smooth
        return self

    def set_option_toolbox(self):
        if self.dbchart.custom_attr_objectdict.show_toolbox:
            self.option.toolbox.show = True
        else:
            self.option.toolbox.show = False
        return self

    def set_option_axis_title(self):
        if self.dbchart.custom_attr is None:
            return self
        if self.dbchart.custom_attr.get('showXAxisTitle', False):
            for axis_option in self.option.xAxis:
                axis_option.name = self.dbchart.custom_attr.get('xAxisTitle', "")
        if self.dbchart.custom_attr.get('showYAxisTitle', False):
            for axis_option in self.option.yAxis:
                axis_option.name = self.dbchart.custom_attr.get('yAxisTitle', "")
        return self

    def _get_word_count(self, unicode_str):
        count = 0
        for c in unicode_str:
            if ord(c) < 128:
                count += 1
            else:
                count += 2
        return count

    def set_option_xaxis_data(self, data_list):
        for axis_option in self.option.xAxis:
            axis_option.data = data_list
        return self

    def set_option_yaxis_data(self, data_list):
        for axis_option in self.option.yAxis:
            axis_option.data = data_list
        return self

    def set_option_xaxis_hidden(self):
        for axis_option in self.option.xAxis:
            if axis_option.data == ["All"]:
                axis_option.axisLabel.show = False
        return self

    def set_option_yaxis_hidden(self):
        for axis_option in self.option.yAxis:
            if axis_option.data == ["All"]:
                self.option.grid[0]["left"] = 20
                axis_option.axisLabel.show = False
        return self

    def set_option_xaxis_rotate(self):
        word_count = self._get_word_count('\n'.join(self.option.xAxis[0].data))
        for axis_option in self.option.xAxis:
            if word_count < 170:
                axis_option.axisLabel.rotate = 0
            else:
                axis_option.axisLabel.rotate = -45
        return self

    def set_option_yaxis_rotate(self):
        word_count = self._get_word_count('\n'.join(self.option.yAxis[0].data))
        for axis_option in self.option.yAxis:
            if word_count < 170:
                axis_option.axisLabel.rotate = 0
            else:
                axis_option.axisLabel.rotate = 45
        return self

    def set_option_xaxis_auto_change(self):
        """
        最大值：最大值 + （最大值 - 最小值）* 0.1 向上取整（10的整数）
        最小值：最小值 - （最大值 - 最小值）* 0.1 向下取整（10的整数）
        """
        if self.dbchart.custom_attr is None:
            return self
        if self.dbchart.custom_attr.get('autoAxis', False):
            for axis_option in self.option.xAxis:
                axis_option.scale = True
        return self

    def set_option_yaxis_auto_change(self):
        """
        最大值：最大值 + （最大值 - 最小值）* 0.1 向上取整（10的整数）
        最小值：最小值 - （最大值 - 最小值）* 0.1 向下取整（10的整数）
        # get_max = "$$function(value) {let gap = (value.max-value.min) * 0.1; let retmax = value.max + gap; retmax += (10 - retmax % 10); return retmax;}$$"
        # get_min = "$$function(value) {let gap = (value.max-value.min) * 0.1; let retmax = value.max + gap; let retmin = value.min - gap; retmax += (10 - retmax % 10); retmin -= (retmin % 10); if (value.min > 0 && retmin < 0) {return 0;} else { return retmin;}}$$"
        """
        if self.dbchart.custom_attr is None:
            return self
        if self.dbchart.custom_attr.get('autoAxis', False):
            for axis_option in self.option.yAxis:
                axis_option.scale = True
        return self

    def set_option_datazoom(self, multi_colortag=True):
        if len(self.option.series) == 0:
            return self

        if len(self.grid_value_list) > 0:
            coefficient = 1 - 1.0 * len(self.grid_value_list) / len(self.option.series)
        else:
            coefficient = 1

        if multi_colortag and self._has_colortag():
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
        return self

    def _get_formatter_dict(self, obj, key="formatter"):
        formatter_dict = dict()
        formatter_dict["showText"] = self.dbchart.custom_attr.get("show_text_on_bar", False)
        if key in obj.custom_attr:
            formatter_dict["ttype"] = ttype = obj.custom_attr[key].get('type', "num")
            if ttype in obj.custom_attr[key]:
                formatter_dict["digit"] = obj.custom_attr[key][ttype].get('digit', 2)
                formatter_dict["millesimal"] = obj.custom_attr[key][ttype].get('millesimal', False)
        return formatter_dict

    def _get_formatter_funcstr(self, **kwargs):
        return "$$this.getNormalFormatterHandler({{ttype: '{ttype}', digit: {digit}, millesimal: {millesimal}, showText: {showText}, showAxis: {showAxis}}})$$".format(
            ttype=kwargs.get("ttype", "num"),
            digit=kwargs.get("digit", 2),
            millesimal=const.TEXT_BOOLEAN[kwargs.get("millesimal", False)],
            showText=const.TEXT_BOOLEAN[kwargs.get("showText", False)],
            showAxis=const.TEXT_BOOLEAN[kwargs.get("showAxis", False)]
        )

    def _get_formatter_lastdict(self, **kwargs):
        return {
            "ttype": kwargs.get("ttype", "num"),
            "digit": kwargs.get("digit", 2),
            "millesimal": kwargs.get("millesimal", False),
            "showText": kwargs.get("showText", False),
            "showAxis": kwargs.get("showAxis", False)
        }

    def set_option_xaxis_formatter(self):
        formatter_kwargs = self._get_formatter_dict(self.dbchart, key="default_field_formatter")
        if self.dbchart.ttype in [chart_consts.CHART_TYPE_BAR_STACK_PERCENT, chart_consts.CHART_TYPE_HBAR_STACK_PERCENT]:
            formatter_kwargs.update(dict(ttype="percent"))
        formatter_kwargs.update(dict(showText=False, showAxis=False))
        for axis in self.option.xAxis:
            axis["axisLabel"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)

    def set_option_yaxis_formatter(self):
        formatter_kwargs = self._get_formatter_dict(self.dbchart, key="default_field_formatter")
        if self.dbchart.ttype in [chart_consts.CHART_TYPE_BAR_STACK_PERCENT, chart_consts.CHART_TYPE_HBAR_STACK_PERCENT]:
            formatter_kwargs.update(dict(ttype="percent"))
        formatter_kwargs.update(dict(showText=False, showAxis=False))
        for axis in self.option.yAxis:
            axis["axisLabel"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)

    def set_option_series_formatter(self):
        for series in self.option.series:
            if self._has_colortag():
                if len(self.value_list) == 1:
                    field = self.value_list[0]
                else:
                    continue
            else:
                field = Field.get_field_by_field_id(series.get('field_id'))

            formatter_kwargs = self._get_formatter_dict(self.dbchart, key="default_field_formatter")
            formatter_kwargs.update(self._get_formatter_dict(field))
            if field.ttype in [field_consts.FIELD_TTYPE_GRID_BAR, field_consts.FIELD_TTYPE_GRID_HBAR,
                               field_consts.FIELD_TTYPE_GRID_LINE]:
                show_text = self.dbchart.custom_attr.get("show_text_on_grid_bar", False)
                formatter_kwargs.update(dict(showText=show_text))
            if self.dbchart.ttype in [chart_consts.CHART_TYPE_BAR_STACK_PERCENT,
                                      chart_consts.CHART_TYPE_HBAR_STACK_PERCENT]:
                formatter_kwargs.update(dict(ttype="percent"))
            if self.dbchart.ttype in [chart_consts.CHART_TYPE_GAUGE]:
                formatter_kwargs.update(dict(ttype="num", millesimal=False, showText=False, showAxis=False))
            series["label"]["normal"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)

            formatter_kwargs.update(dict(showText=True, showAxis=True))
            if self.dbchart.ttype in [chart_consts.CHART_TYPE_GAUGE]:
                formatter_kwargs.update(dict(ttype="num", millesimal=False, showText=False, showAxis=False))
            series["tooltip"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)
            formatter_kwargs.update(dict(showText=True, showAxis=False))
            self.formatterDict[series.name] = self._get_formatter_lastdict(**formatter_kwargs)

        if self.dbchart.ttype in [chart_consts.CHART_TYPE_BAR_STACK, chart_consts.CHART_TYPE_BAR_STACK_PERCENT,
                                  chart_consts.CHART_TYPE_HBAR_STACK, chart_consts.CHART_TYPE_HBAR_STACK_PERCENT,
                                  chart_consts.CHART_TYPE_BARLINE, chart_consts.CHART_TYPE_BARLINE_STACK,
                                  chart_consts.CHART_TYPE_LINE, chart_consts.CHART_TYPE_LINE_SHADOW,
                                  chart_consts.CHART_TYPE_LINE_STACK]:
            self.option["tooltip"]["formatter"] = "$$this.getGlobalFormatterHandler$$"

    def set_markline(self):
        if self.dbchart.custom_attr.get('mark_line', False):
            for x in self.dbchart.markline:
                data_shaft = None
                line_data = None
                line_field = x.get('field')
                line_name = x.get('name')
                line_color = x.get('color')
                line_type = x.get('type')
                line_line_type = x.get('line_type')
                line_width = x.get('line_width', 1)

                # 判断有没有对比
                if self.vtype in [
                    Vtype.Y_VALUE_Y_COLOR_Y_INDEX,
                    Vtype.N_VALUE_Y_COLOR_Y_INDEX,
                    Vtype.Y_VALUE_Y_COLOR_N_INDEX,
                    Vtype.N_VALUE_Y_COLOR_N_INDEX
                ]:
                    result = self.dh.get_pivot_data_result()
                    all_result_data_list = []
                    for data in result['data']:
                        all_result_data_list.extend([v if v != settings.NONE_DATA else 0 for v in data['value']])
                    if line_type == 'min':
                        line_data = min(all_result_data_list)
                    elif line_type == 'max':
                        line_data = max(all_result_data_list)
                    elif line_type == 'average':
                        line_data = sum(all_result_data_list) / len(all_result_data_list)
                    elif line_type == 'custom':
                        line_data = x.get('data')
                    if 'hbar' in self.dbchart.ttype:
                        data_shaft = 'xAxis'
                    elif 'bar' in self.dbchart.ttype or 'line' in self.dbchart.ttype:
                        data_shaft = 'yAxis'
                    type_line_data = {
                        'name': line_name,
                        data_shaft: line_data,
                        'lineStyle': {
                            'normal': {
                                'type': line_line_type,
                                'width': line_width,
                                'color': line_color
                            }
                        }
                    }
                    self.option.series[0].markLine.data.append(type_line_data)
                else:
                    # 根据所托的纬度和度量求中位数（不同的纬度和度量的组合方式数值不一样）
                    if line_type == 'custom':
                        if 'hbar' in self.dbchart.ttype:
                            data_shaft = 'xAxis'
                        elif 'bar' in self.dbchart.ttype or 'line' in self.dbchart.ttype:
                            data_shaft = 'yAxis'
                        line_data = x.get('data')
                        type_line_data = {
                            'name': line_name,
                            data_shaft: line_data,
                            'lineStyle': {
                                'normal': {
                                    'type': line_line_type,
                                    'width': line_width,
                                    'color': line_color
                                }
                            }
                        }
                    elif line_type == 'calc':
                        if 'hbar' in self.dbchart.ttype:
                            data_shaft = 'xAxis'
                        elif 'bar' in self.dbchart.ttype or 'line' in self.dbchart.ttype:
                            data_shaft = 'yAxis'
                        field_id = x.get('field_id')
                        field = Field.get_field_by_field_id(field_id)

                        if field is None:
                            continue
                        pivot = Pivot_main(field_id, ["All"], field.aggable, field.get_func(),
                                           field.multifunc, field.sortfunc, field.sort_regiontype_id)
                        series = self.dh._get_serie_data(pivot)

                        line_data = float(series.values[0])
                        type_line_data = {
                            'name': line_name,
                            data_shaft: line_data,
                            'lineStyle': {
                                'normal': {
                                    'type': line_line_type,
                                    'width': line_width,
                                    'color': line_color
                                }
                            }
                        }
                    else:
                        type_line_data = {
                            'name': line_name,
                            'type': line_type,
                            'lineStyle': {
                                'normal': {
                                    'type': line_line_type,
                                    'width': line_width,
                                    'color': line_color
                                }
                            }
                        }

                    if line_field is None:  # 对于固定值与计算类型值可能有效
                        if len(self.option.series) > 0:
                            self.option.series[0].markLine.data.append(type_line_data)
                    else:
                        field_name = self._convert_field_name(line_field)  # 指定要为哪个字段设置markline

                        for index, series in enumerate(self.option.series):
                            if series.name == field_name:
                                self.option.series[index].markLine.data.append(type_line_data)
        return self
