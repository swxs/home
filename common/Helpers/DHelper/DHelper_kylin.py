# encoding=utf8

import os
import numpy as np
import pandas as pd
import settings
from sql import *
from sql.aggregate import *
from sql.conditionals import *
from apps.bi import model_enums
from apps.bi import field_utils
from apps.bi import column_utils
from apps.bi import group_utils
from commons import df_utils
from commons.log_utils import get_logging
from commons.Helpers.Helper_validate import Validate, RegType
from commons.DHelper.DHelper_base import DHelper_base
from commons.Helpers.DBHelper_kylin import KylinDBHelper
from commons.ParserUtils.ODBC_parser import get_parser as _get_parser, Part, Filter, Calc, Aggregate, Column

# 上面这几个import不要删除
from collections import deque
from functools import reduce

from sql.operators import Or
from sql.operators import And
from tornado.util import ObjectDict
from commons.consts import AGG_OPERATION_DICT
from commons.consts import DATE_COLUMN_TIMESTAMP

log = get_logging('DHelper_kylin.py')

DTYPE_DATETIME_LIST = [
    model_enums.FIELD_DTYPE_DATETIME_Y,
    model_enums.FIELD_DTYPE_DATETIME_Q,
    model_enums.FIELD_DTYPE_DATETIME_M,
    model_enums.FIELD_DTYPE_DATETIME_W,
    model_enums.FIELD_DTYPE_DATETIME_WD,
    model_enums.FIELD_DTYPE_DATETIME_D
]


def get_project_region_dataframe():
    path = os.path.join(settings.DATA_FILE_PATH, f"region.h5")
    return df_utils.get_dataframe_by_file(path)


def get_aggfunc_by_name(name):
    AGGFUNC_DICT = {
        model_enums.FIELD_AGG_TYPE_COUNT: np.size,
        model_enums.FIELD_AGG_TYPE_NUNIQ: pd.Series.nunique,
        model_enums.FIELD_AGG_TYPE_SUM: np.sum,
        model_enums.FIELD_AGG_TYPE_MEAN: np.mean,
        model_enums.FIELD_AGG_TYPE_MAX: np.max,
        model_enums.FIELD_AGG_TYPE_MIN: np.min,
    }

    return AGGFUNC_DICT.get(name)


def _format_value(temp):
    '''
    用于把数值类型的字符串转为float类型
    :param temp: 要转换的字符串
    :param field_dict:
    :return:
    '''
    if not isinstance(temp, str):
        return temp
    elif temp.isdigit():
        # TODO 以后数据进来都应该是float， 测试数据有问题在kylin里是整形，后面注意修改
        # return float(temp)
        return int(temp)
    else:
        return temp


class DHelper_kylin(DHelper_base):
    # def __new__(cls, *args, **kwargs):
    #     singleton = cls.__dict__.get('__singleton__')
    #     if singleton is not None:
    #         return singleton
    #     cls.__singleton__ = singleton = object.__new__(cls)
    #     return singleton

    def __init__(self, kylin_obj=None):
        if kylin_obj is not None:
            super(DHelper_kylin, self).__init__(kylin_obj)
            self.kylin_obj = kylin_obj
            kylin_client_parms = {
                "join_table": self.kylin_obj.join_table,
                "column_table": self.kylin_obj.column_table,
                "column_list": self.kylin_obj.column_list
            }
            self.kylin_client = KylinAggregateDBHelper(**kylin_client_parms)
            self.pivot_df = None
            self.filters = []
            self.aid_filters = []
            self.region_filter_list = []
            self.new_column_dict = {}
            self._has_aid = None
            self.project = {}

    def do_preprocess(self):
        if self._has_aid_df():
            # self._do_add_aid_df(self.df)
            # 所有操作作用在一个偏移了时间的拷贝上
            self._do_aid_filter()
            self._do_aid_add_new_column()
            self._do_aid_drilldown()
            self._do_aid_field_filter()
        self._do_filter()
        self._do_add_new_column()
        self._do_drilldown()
        self._do_field_filter()
        return self

    def _has_aid_df(self):
        if self._has_aid is None:
            self._has_aid = True
            self._aid_datagroup = None
            for new_column in self._new_column_list:
                if new_column.dtype in [model_enums.FIELD_DTYPE_DATETIME]:
                    self._aid_datagroup = new_column.date_type
                    break
            else:
                self._has_aid = False
                return self._has_aid

            for new_column in self._new_column_list:
                if new_column.multifunc in [
                    model_enums.FIELD_MULTI_AGG_TYPE_CHAIN_RATIO,
                    model_enums.FIELD_MULTI_AGG_TYPE_CHAIN_CHANGE
                ]:
                    break
            else:
                self._has_aid = False
                return self._has_aid
        return self._has_aid

    def _do_aid_filter(self):
        for _filter in self._filter_list:
            if _filter.dtype == model_enums.FIELD_DTYPE_DATETIME:
                start_time = _filter.value_list[1]
                end_time = _filter.value_list[2]
                if start_time:
                    self.aid_filters.append({
                        "binary_operator": "GreaterEqual",
                        "value": int(start_time.timestamp()),
                        "column_id": _filter.column_id,
                        "dtype": "timestamp",
                    })
                if end_time:
                    self.aid_filters.append({
                        "binary_operator": "LessEqual",
                        "value": int(end_time.timestamp()),
                        "column_id": _filter.column_id,
                        "dtype": "timestamp",
                    })
            elif _filter.dtype in DTYPE_DATETIME_LIST:
                self.aid_filters.append({
                    "binary_operator": "In",
                    "value": _filter.value_list,
                    "column_id": _filter.column_id,
                    "dtype": _filter.dtype,
                })
            else:
                self.aid_filters.append({
                    "binary_operator": "In",
                    "value": _filter.value_list,
                    "column_id": _filter.column_id,
                    "dtype": _filter.dtype,
                })

    def _do_aid_drilldown(self):
        for drilldown in self._drilldown_list:
            self.aid_filters.append({
                "binary_operator": "Equal",
                "value": drilldown.value,
                "column": drilldown.column_id,
                "dtype": drilldown.dtype,
            })

    def _do_aid_field_filter(self):
        for field_filter in self._field_filter_list:
            self.aid_filters.append({
                "binary_operator": "In",
                "value": field_filter.value_list,
                "column_id": field_filter.column_id,
                "dtype": field_filter.dtype
            })

    def _do_aid_add_new_column(self):
        for new_column in self._new_column_list:
            if new_column.dtype == model_enums.FIELD_DTYPE_DATETIME:
                self.new_column_dict[new_column.new_column] = {
                    "col": new_column.column,
                    "column_id": new_column.column_id,
                    "dtype": new_column.dtype,
                    "date_type": new_column.date_type,
                }
            else:
                self.new_column_dict[new_column.new_column] = {
                    "col": new_column.column,
                    "column_id": new_column.column_id,
                    "dtype": new_column.dtype,
                    "date_type": model_enums.COLUMN_DTYPE_DATETIME_M,
                }
        self.new_column_dict["All"] = {
            "col": "All",
            "column_id": "All",
            "dtype": model_enums.COLUMN_DTYPE_STRING,
            "date_type": model_enums.COLUMN_DTYPE_DATETIME_M,
        }

    def _do_filter(self):
        for _filter in self._filter_list:
            if _filter.dtype == model_enums.FIELD_DTYPE_DATETIME:
                start_time = _filter.value_list[1]
                end_time = _filter.value_list[2]
                if start_time:
                    self.filters.append({
                        "binary_operator": "GreaterEqual",
                        "value": int(start_time.timestamp()),
                        "column_id": _filter.column_id,
                        "dtype": "timestamp",
                    })
                if end_time:
                    self.filters.append({
                        "binary_operator": "LessEqual",
                        "value": int(end_time.timestamp()),
                        "column_id": _filter.column_id,
                        "dtype": "timestamp",
                    })
            elif _filter.dtype in DTYPE_DATETIME_LIST:
                self.filters.append({
                    "binary_operator": "In",
                    "value": _filter.value_list,
                    "column_id": _filter.column_id,
                    "dtype": _filter.dtype,
                })
            else:
                self.filters.append({
                    "binary_operator": "In",
                    "value": _filter.value_list,
                    "column_id": _filter.column_id,
                    "dtype": _filter.dtype,
                })

    def _do_field_filter(self):
        for field_filter in self._field_filter_list:
            self.filters.append({
                "binary_operator": "In",
                "value": field_filter.value_list,
                "column_id": field_filter.column_id,
                "dtype": field_filter.dtype
            })

    def _do_add_new_column(self):
        for new_column in self._new_column_list:
            if new_column.dtype == model_enums.FIELD_DTYPE_DATETIME:
                self.new_column_dict[new_column.new_column] = {
                    "col": new_column.column,
                    "column_id": new_column.column_id,
                    "dtype": new_column.dtype,
                    "date_type": new_column.date_type,
                }
            else:
                self.new_column_dict[new_column.new_column] = {
                    "col": new_column.column,
                    "column_id": new_column.column_id,
                    "dtype": new_column.dtype,
                    "date_type": model_enums.COLUMN_DTYPE_DATETIME_M,
                }
        self.new_column_dict["All"] = {
            "col": "All",
            "column_id": "All",
            "dtype": model_enums.COLUMN_DTYPE_STRING,
            "date_type": model_enums.COLUMN_DTYPE_DATETIME_M,
        }

    def _do_drilldown(self):
        for drilldown in self._drilldown_list:
            self.filters.append({
                "binary_operator": "Equal",
                "value": drilldown.value,
                "column_id": drilldown.column_id,
                "dtype": drilldown.dtype,
            })

    def get_aggfunc(self, pivot):
        if pivot.func == model_enums.FIELD_AGG_TYPE_MEAN:
            return {pivot.new_column: {"aggregate": AGG_OPERATION_DICT["Avg"]}}
        elif pivot.func == model_enums.FIELD_AGG_TYPE_COUNT:
            return {pivot.new_column: {"aggregate": AGG_OPERATION_DICT["Count"]}}
        elif pivot.func == model_enums.FIELD_AGG_TYPE_SUM:
            return {pivot.new_column: {"aggregate": AGG_OPERATION_DICT["Sum"]}}
        elif pivot.func == model_enums.FIELD_AGG_TYPE_NUNIQ:
            return {pivot.new_column: {"aggregate": AGG_OPERATION_DICT["Count"], "distinct": True}}
        else:
            return None

    async def _get_series(self, pivot, is_aid=False):
        def get_sorted_series(agg_series, index_list):
            left_field_id = None  # 合表的列名， 如果是使用维度字段， 则是field_id, 否则为层级中的一个层级名
            right_field_id = None  # 合表的列名， 层级名
            region_column_list = []  # 只需要导入下列字段

            min_region_type = None  # 最小的层级名
            min_field_id = None  # 最小层级对应的field_id (使用维度情况下)
            current_level = 0  # 记录当前层级， 最高层做特殊处理（level==0时， 使用无层级处理的模式处理）
            for field_id in index_list:  # index_list， 只有维度情况下只包含维度（对比），在数据范围模式下包含了数据范围对应的层级名
                if Validate.check(field_id, reg_type=RegType.COLUMN_ID):
                    region_type_display_name = field_utils.get_field_by_field_id(field_id).column_id
                    current_region_type = group_utils.get_region_type_by_display_name_project_id(
                        region_type_display_name
                    )
                else:
                    current_region_type = group_utils.get_region_type_by_display_name_project_id(field_id)
                # 到这里 region_type 是对应的层级， field_id 是 表中的列名

                if (current_region_type is not None) and (current_region_type.level > current_level):
                    min_region_type = current_region_type  # 当前最小的层级
                    min_field_id = field_id  # 最小层级所对应的列名
                    current_level = current_region_type.level  # 当前层级

            if min_region_type is not None:
                left_field_id = min_field_id
                right_field_id = min_region_type.display_name
                for region_type in group_utils.get_region_type_list_by_project_id():
                    if 0 < region_type.level <= min_region_type.level:
                        region_column_list.append(region_type.display_name)

            if pivot.sort_regiontype_id is not None:  # 如果是要查看在全国内的排名， 则使用（level==0时， 使用无层级处理的模式处理）
                region_type = group_utils.get_region_type_by_id(pivot.sort_regiontype_id)
                if region_type.level == 0:
                    left_field_id = None

            if (left_field_id is None) or (pivot.sort_regiontype_id is None):
                agg_series = agg_series.rank(ascending=pivot.sortfunc, method="min")
            else:
                sort_region_type = group_utils.get_region_type_by_id(pivot.sort_regiontype_id)

                output_series_name = agg_series.name
                output_series_index = agg_series.index

                #  这里获取层级结构表中指定的层级并去重， 否则数据行数会增加
                region_base_df = get_project_region_dataframe()
                region_df = region_base_df[region_column_list].drop_duplicates()
                df_from_series = pd.DataFrame(agg_series).reset_index()
                df_with_region = pd.merge(left=df_from_series, right=region_df, left_on=left_field_id,
                                          right_on=right_field_id, how="left")
                # df_with_region = pd.merge(left=df_from_series, right=region_df, left_on=left_field_id, right_on=right_field_id, how="left").groupby([left_field_id]).mean().reset_index()
                df_with_region.columns.tolist()

                # 到这里要计算指定层级下每个子层级的排名， 并组合
                grouped_with_region_df = df_with_region.groupby([sort_region_type.display_name])
                reseted_index_series = pd.Series()
                for index, df in grouped_with_region_df:
                    reseted_index_series = df[output_series_name].rank(ascending=pivot.sortfunc, method="min")
                df_with_region[output_series_name] = reseted_index_series
                agg_series = df_with_region.set_index(index_list)[output_series_name]
            return agg_series

        async def get_series(pivot, index_list, is_aid):
            if pivot.aggable:
                result = await self.kylin_client.aggregate(
                    self.filters,
                    index_list,
                    self.get_aggfunc(pivot),
                    self.new_column_dict,
                    is_aid,
                )
                agg_series = result.set_index(index_list)[pivot.new_column]
            else:
                result = await self.kylin_client.aggregate_calc(
                    self.filters,
                    index_list,
                    pivot.new_column,
                    self.new_column_dict,
                    is_aid,
                )
                agg_series = result.set_index(index_list)[pivot.new_column]

            """
                转换为排序
                sortfunc = True 从小到大
                sortfunc = False 从大到小
            """
            if pivot.sortfunc is not None:
                agg_series = get_sorted_series(agg_series, index_list)
            return agg_series

        for region_filter in self.region_filter_list:
            if region_filter.new_column == pivot.new_column:
                index_list = pivot.index_list[:] + [region_filter.column]
                output_series = await get_series(pivot, index_list, is_aid)
                output_df = pd.DataFrame(output_series).reset_index()
                agg_series = output_df[output_df[region_filter.column].isin(region_filter.value_list)].set_index(pivot.index_list)[pivot.new_column]
                return agg_series

        agg_series = await get_series(pivot, pivot.index_list, is_aid)
        return agg_series

    async def _get_serie_data(self, pivot):
        if self._has_aid_df() and pivot.multifunc == model_enums.FIELD_MULTI_AGG_TYPE_CHAIN_RATIO:
            series = await self._get_series(pivot, is_aid=False)
            serie_tmp = await self._get_series(pivot, is_aid=True)
            df_tmp = pd.DataFrame([series, serie_tmp], index=[0, 1]).T.dropna()
            df_tmp[pivot.new_column] = ((1.0 * df_tmp.iloc[:, 0] / df_tmp.iloc[:, 1]) - 1) * 100
            return df_tmp[pivot.new_column]
        elif self._has_aid_df() and pivot.multifunc == model_enums.FIELD_MULTI_AGG_TYPE_CHAIN_CHANGE:
            series = await self._get_series(pivot, is_aid=False)
            serie_tmp = await self._get_series(pivot, is_aid=True)
            df_tmp = pd.DataFrame([series, serie_tmp], index=[0, 1]).T.dropna()
            df_tmp[pivot.new_column] = df_tmp.iloc[:, 0] - df_tmp.iloc[:, 1]
            return df_tmp[pivot.new_column]
        else:
            return await self._get_series(pivot, is_aid=False)

    async def _get_main_df(self, pivot_list, has_colortag, fillna=settings.NONE_DATA):
        main_serie_list = []
        for pivot in pivot_list:
            serie = (await self._get_serie_data(pivot)).dropna()
            main_serie_list.append(serie)

        if main_serie_list:
            # 经过排序处理之后的各series的index可能不再相同顺序， 导致合并的df缺失columns.name[s], 此处以
            # 第一个series的index作为合并df的column
            tmp_df = pd.DataFrame(main_serie_list, columns=main_serie_list[0].index)
        else:
            tmp_df = pd.DataFrame()

        def get_column_name(column):
            """
            整理dataframe的列名，对单列则拆包， 否则直接返回
            如果是多层的MultiIndex类型， 则直接返回，
            否则尝试浮点，
            不行则返回字符串
            :param column:
            :return:
            """
            try:
                if isinstance(column, tuple):
                    if len(column) == 1:
                        column = column[0]
                        return float(column)
                    else:
                        return column
                else:
                    return float(column)
            except Exception:
                return str(column)

        if has_colortag and len(pivot_list) > 0:  # 存在对比
            all_data = tmp_df.values[0].tolist()
            if hasattr(tmp_df.columns, "levels"):
                # 非对比列所有可选项
                new_columns = list()
                for column in tmp_df.columns.droplevel(level=-1).tolist():
                    if column not in new_columns:
                        new_columns.append(column)

                # 将非对比列所有情况映射到各个对比列选项字典中
                new_columns_names = tmp_df.columns.names[:-1]
                data_dict = dict()
                for i, data in enumerate(all_data):
                    colortag_name = get_column_name(tmp_df.columns[i][-1])
                    if colortag_name not in data_dict:
                        data_dict[colortag_name] = dict()
                    data_dict[colortag_name][get_column_name(tmp_df.columns[i][0:-1])] = data
                if len(new_columns_names) == 1:
                    tmp_df = pd.DataFrame(data_dict, index=pd.Index(new_columns)).T
                else:
                    #  https://github.com/pandas-dev/pandas/issues/12457
                    tmp_df = pd.DataFrame(data_dict, index=pd.MultiIndex.from_tuples(new_columns)).T
            else:
                new_columns_names = ["All"]
                new_columns = ["All"]
                colortag_columns = tmp_df.columns.tolist()
                data_dict = dict()

                for columns in colortag_columns:
                    data_dict[get_column_name(columns)] = list()
                for columns in colortag_columns:
                    data_dict[get_column_name(columns)].append(np.nan)
                for i, data in enumerate(all_data):
                    data_dict[get_column_name(colortag_columns[i])].pop()
                    data_dict[get_column_name(colortag_columns[i])].append(data)
                tmp_df = pd.DataFrame(data_dict, index=new_columns).T
            tmp_df.columns.set_names(new_columns_names, inplace=True)

        # [swxs] TODO: 下列信息不删掉可能有很大用处
        pivot_list = []
        return tmp_df

    async def _get_sub_df(self, pivot_list, has_colortag, fillna=settings.NONE_DATA):
        sub_serie_list = []
        for pivot in pivot_list:
            serie = (await self._get_serie_data(pivot)).dropna()
            sub_serie_list.append(serie)

        # tmp_df = pd.DataFrame(main_serie_list)
        if sub_serie_list:
            # 经过排序处理之后的各series的index可能不再相同顺序， 导致合并的df缺失columns.name[s], 此处以
            # 第一个series的index作为合并df的column
            tmp_df = pd.DataFrame(sub_serie_list, columns=sub_serie_list[0].index)
        else:
            tmp_df = pd.DataFrame()

        # [swxs] TODO: 下列信息不删掉可能有很大用处
        pivot_list = []
        return tmp_df

    async def do_pivot(self, has_color_tag, fillna=settings.NONE_DATA):
        self.pivot_df = pd.concat([
            await self._get_main_df(self._pivot_main_list, has_color_tag, fillna=fillna),
            await self._get_sub_df(self._pivot_sub_list, has_color_tag, fillna=fillna)
        ]).fillna(value=fillna)

        self.pivot_x_df = await self._get_main_df(self._pivot_main_x_list, has_color_tag, fillna=fillna)
        self.pivot_y_df = await self._get_main_df(self._pivot_main_y_list, has_color_tag, fillna=fillna)

        self.group_df = pd.concat([
            self.pivot_x_df,
            self.pivot_y_df,
            await self._get_sub_df(self._pivot_sub_list, has_color_tag, fillna=fillna)
        ]).fillna(value=fillna)
        return self.pivot_df, self.pivot_x_df, self.pivot_y_df

    def do_rank(self, dtype, ascending, sortIndex, xAxisCount=None, dropna=settings.NONE_DATA):
        if dtype == 1:
            if hasattr(self, "pivot_df") and len(self.pivot_df) > 0:
                self.pivot_df = self.pivot_df.T[~self.pivot_df.T.iloc[:, sortIndex].isin([dropna])].T
                ranked_series = self.pivot_df.iloc[sortIndex].rank()
                ranked_index = ranked_series.sort_values('index', ascending=ascending).index
                self.pivot_df = self.pivot_df.T.reindex(ranked_index).T
                if xAxisCount:
                    self.pivot_df = self.pivot_df.iloc[:, 0:xAxisCount]
        elif dtype == 2:
            if hasattr(self, "pivot_df") and len(self.pivot_df.T) > 0:
                self.pivot_df = self.pivot_df[~self.pivot_df.iloc[:, 0].isin([dropna])]
                ranked_series = self.pivot_df.rank().iloc[:, 0]
                ranked_index = ranked_series.sort_values('index', ascending=ascending).index
                self.pivot_df = self.pivot_df.reindex(ranked_index)
                if xAxisCount:
                    self.pivot_df = self.pivot_df.iloc[0:xAxisCount, :]
        return self.pivot_df

    def do_refresh(self, field_id_list):
        return self

    async def get_raw_data_result(self, column_list, start=0, end=None):
        """
        以通用格式将未做聚合操作的数据源返回其中指定的部分数据列
        :param column_list: 指定的数据列
        :param start: 开始行数
        :param end: 结束行数
        :return:
        """
        df = await self.get_base_data(start=start, end=end)
        index_range = slice(*(slice(start, end).indices(len(df))))
        column_name_list = [self.new_column_dict[column_id]["col"] for column_id in column_list]
        self.pivot_df = df.reset_index().iloc[index_range, :].loc[:, column_name_list]
        result = self.get_pivot_data_result()
        result.update(dict(info=dict(length=len(df))))
        return result

    async def get_base_data(self, start=0, end=None):
        base_data = self.kylin_client.get_base_data(start, end)
        df = pd.DataFrame(base_data)
        return df

    def get_field_unique_value_list(self, column, dtype=None):
        return self.kylin_client.get_column_value_list(column.id, dtype, self.filters)


class KylinAggregateDBHelper(object):
    def __init__(self, **params):
        self.kylin_project = params.get("kylin_project", settings.KYLIN_PROJECT)
        self.kylin = KylinDBHelper(kylin_project=self.kylin_project)

        self.column_table = params.get("column_table", ObjectDict())  # 所有字段属性
        self.join_table = params.get("join_table", ObjectDict())  # 原始的数据表
        self.column_list = params.get("column_list", [])  # 所有字段， 可能可以省略

    def get_base_data(self, start, end):
        '''
        组合原始表
        :param start:
        :param end:
        :return:
        '''
        group_column = []
        select_column = []
        for column in self.column_list:
            if column.ttype in (model_enums.COLUMN_TTYPE_CALC,):
                pass
            elif column.ttype in (model_enums.COLUMN_TTYPE_GROUP,):
                # INFO 后面性能出问题的话可以考虑去掉
                group_column.append(self.column_table[column.id]["case"].as_(column.col))
            else:
                column_with_table = self._get_table(column.id)
                select_column.append(column_with_table.as_(column.col))

        select = self.join_table.select(*select_column, *group_column, limit=end, offset=start)
        result = self.kylin.execute(select)

        return result

    def get_column_value_list(self, column_id, dtype, filters, is_aid=False):
        '''
        获取下拉选择的值
        :param column_name:
        :param dtype:
        :param filters:
        :parame is_aid:
        :return:
        '''
        column_with_table = self._get_table(column_id, dtype, is_aid=is_aid)
        select = self.join_table.select(column_with_table, group_by=column_with_table)
        # TODO 附加筛选的情况未测试
        conditions = self._get_conditions(filters, {}, is_aid)
        if conditions:
            select.where = conditions
        return self.kylin.execute_value_list(select)

    def _get_table(self, column_id, dtype=model_enums.COLUMN_DTYPE_STRING, date_type=model_enums.FIELD_DATE_TYPE_MONTH, is_aid=False):
        table = self._get_column_table(column_id, dtype, is_aid)
        column = self._get_column_column(column_id, dtype, date_type=date_type, is_aid=is_aid)
        if self.column_table[column_id]["ttype"] == model_enums.COLUMN_TTYPE_GROUP:
            return self.column_table[column_id]["case"]
        else:
            return getattr(table, column)

    def _get_column_table(self, column_id, dtype=model_enums.COLUMN_DTYPE_STRING, is_aid=False):
        if is_aid and dtype in (
                "timestamp",
                model_enums.COLUMN_DTYPE_DATETIME,
                model_enums.COLUMN_DTYPE_DATETIME_Y,
                model_enums.COLUMN_DTYPE_DATETIME_Q,
                model_enums.COLUMN_DTYPE_DATETIME_M,
                model_enums.COLUMN_DTYPE_DATETIME_W,
                model_enums.COLUMN_DTYPE_DATETIME_WD,
                model_enums.COLUMN_DTYPE_DATETIME_D,
        ):
            return self.column_table[column_id]["table_date_aid"]
        elif not is_aid and dtype in (
                "timestamp",
                model_enums.COLUMN_DTYPE_DATETIME,
                model_enums.COLUMN_DTYPE_DATETIME_Y,
                model_enums.COLUMN_DTYPE_DATETIME_Q,
                model_enums.COLUMN_DTYPE_DATETIME_M,
                model_enums.COLUMN_DTYPE_DATETIME_W,
                model_enums.COLUMN_DTYPE_DATETIME_WD,
                model_enums.COLUMN_DTYPE_DATETIME_D,
        ):
            return self.column_table[column_id]["table_date"]
        else:
            return self.column_table[column_id]["table"]

    def _get_column_column(self, column_id, dtype=model_enums.COLUMN_DTYPE_STRING, date_type=model_enums.FIELD_DATE_TYPE_MONTH, is_aid=False):
        if dtype == model_enums.COLUMN_DTYPE_DATETIME:
            if date_type == model_enums.FIELD_DATE_TYPE_YEAR:
                return "YEAR"
            elif date_type == model_enums.FIELD_DATE_TYPE_QUARTER:
                return "QUARTER"
            elif date_type == model_enums.FIELD_DATE_TYPE_MONTH:
                return "MONTH"
            elif date_type == model_enums.FIELD_DATE_TYPE_DAY:
                return "DAY"
            elif date_type == model_enums.FIELD_DATE_TYPE_WEEK:
                return "WEEK"
            else:
                return "TIMESTAMP"
        elif dtype == model_enums.COLUMN_DTYPE_DATETIME_Y:
            return "DATETIME_Y"
        elif dtype == model_enums.COLUMN_DTYPE_DATETIME_Q:
            return "DATETIME_Q"
        elif dtype == model_enums.COLUMN_DTYPE_DATETIME_M:
            return "DATETIME_M"
        elif dtype == model_enums.COLUMN_DTYPE_DATETIME_D:
            return "DATETIME_D"
        elif dtype == model_enums.COLUMN_DTYPE_DATETIME_W:
            return "DATETIME_W"
        elif dtype == model_enums.COLUMN_DTYPE_DATETIME_WD:
            return "DATETIME_WD"
        elif dtype == "timestamp":
            return "TIMESTAMP"
        else:
            return self.column_table[column_id]["column"]

    def _get_group_by(self, group_list, convert_column, is_aid):
        '''
        获取分组条件
        :param group_list: 聚合字段列表
        :param convert_column: field_id->column映射表
        :param is_aid: 是否偏移
        :return: 聚合字段column
        '''
        group_column_list = []
        for _group_field_id in group_list:
            column_with_table = self._get_table(
                convert_column[_group_field_id]["column_id"],
                convert_column[_group_field_id]["dtype"],
                convert_column[_group_field_id]["date_type"],
                is_aid
            )
            group_column_list.append(column_with_table)

        return group_column_list

    def _get_group_by_select_list(self, group_list, convert_column, is_aid):
        # TODO: 除了设置输出名都与上面方法相同， 可以合并
        '''
        获取分组条件作为查询字段，设置输出名
        :param group_list: 聚合字段列表
        :param convert_column: field_id->column映射表
        :param is_aid: 是否偏移
        :return: 聚合字段column.as
        '''
        group_column_list = []
        for _group_field_id in group_list:
            column_with_table = self._get_table(
                convert_column[_group_field_id]["column_id"],
                convert_column[_group_field_id]["dtype"],
                convert_column[_group_field_id]["date_type"],
                is_aid
            )
            group_column_list.append(column_with_table.as_(_group_field_id))

        return group_column_list

    def _get_select_list(self, aggregate, convert_column, is_aid):
        '''
        获取查询字段，设置输出名
        :param aggregate: 附带字段及对应的计算方法
        :param convert_column: field_id->column映射表
        :param is_aid: 是否偏移
        :return: 聚合字段column.as
        '''
        select_list = []
        for _aggregate_field_id, aggfunc in aggregate.items():
            column_id = convert_column[_aggregate_field_id]['column_id']
            dtype = convert_column[_aggregate_field_id]['dtype']
            column_with_table = self._get_table(column_id, dtype, is_aid)
            Aggregate = aggfunc.get("aggregate")
            select_list.append(Aggregate(column_with_table, aggfunc.get("distinct", False)).as_(_aggregate_field_id))
        return select_list

    def _calc_aggregate_select_list(self, result, column_id):
        '''
        获取筛选条件
        :param result: 最终计算表达式
        :param column_id: 计算字段id
        :return:
        '''

        def parse_aggregate(result):
            if isinstance(result, Aggregate):
                for node in self.column_table[column_id]["exp"]:
                    if node["aggregate"] == result:
                        return getattr(node["table"], node["column"])
            elif isinstance(result, Calc):
                left_part = parse_aggregate(result.left)
                right_part = parse_aggregate(result.right)
                if result.ttype == "+":
                    return left_part + right_part
                elif result.ttype == "-":
                    return left_part - right_part
                elif result.ttype == "*":
                    return left_part * right_part
                elif result.ttype == "/":
                    return left_part / right_part.cast("double")
            else:
                return _format_value(result)

        return parse_aggregate(result)

    def _get_conditions(self, filters, convert_column, is_aid):
        '''
        获取基础查询条件
        :param filters: 筛选条件
        :param convert_column: field_id->column映射表
        :param is_aid: 是否偏移
        :return: 筛选条件对象
        '''
        # 去重
        func = lambda x, y: x if y in x else x + [y]
        filters = reduce(func, [[], ] + filters)
        condition_list = []
        for _filter in filters:
            column_id = _filter.get("column_id")
            Operator = AGG_OPERATION_DICT[_filter.get('binary_operator')]
            column_with_table = self._get_table(column_id, _filter.get("dtype"), is_aid)
            condition_list.append(Operator(column_with_table, _filter.get("value")))

        if len(condition_list) == 0:
            condition_list = None
        elif len(condition_list) == 1:
            condition_list = condition_list[0]
        elif len(condition_list) > 1:
            condition_list = And(condition_list)
        return condition_list

    def _get_calc_part_conditions(self, expression, convert_column, is_aid):
        '''
        获取计算字段子集的追加查询条件
        :param expression: 结构树
        :param is_aid: 是否偏移
        :return: 筛选条件对象
        :return:
        '''

        def parse_node(expression):
            if isinstance(expression, Part):
                if expression.ttype == "&":
                    return And(*[parse_node(child) for child in expression.children])
                elif expression.ttype == "|":
                    return Or(*[parse_node(child) for child in expression.children])
                elif expression.ttype is None:
                    if len(expression.children) == 1:
                        if isinstance(expression.children[0], Filter):
                            if isinstance(expression.children[0].left, Column):
                                column_part = expression.children[0].left
                                table = self._get_column_table(column_part.column_id, column_part.dtype, is_aid)
                                column_name = self._get_column_column(column_part.column_id, column_part.dtype, is_aid=is_aid)
                                column = getattr(table, column_name)
                            else:
                                # 后面不应该走进来
                                column = getattr(
                                    self.column_table[expression.children[0].left]['table'],
                                    self.column_table[expression.children[0].left]['column']
                                )
                            filter = expression.children[0].ttype
                            target = expression.children[0].right
                            return AGG_OPERATION_DICT[filter](column, target)
                        else:
                            return None
            else:
                return None

        return parse_node(expression)

    def _get_base_sql_table(self, convert_column=None, filters=None, group_list=None, aggregate=None, calc_columns_set=None, is_aid=False):
        """
        检测所有流程中使用的字段， 如果存在分组字段， 则在基础查询表上附加分组字段，
        否则直接返回基础查询表
        :param convert_column:
        :param filters: 筛选条件
        :param group_list: 聚合字段列表
        :param aggregate: 附带字段及对应的计算方法
        :param calc_columns_set: 计算字段使用的字段列表
        :param is_aid: 是否偏移
        :return: 查询表
        """
        column_id_set = set()
        if filters:
            for _filter in filters:
                column_id_set.add(_filter.get("column_id"))
        if group_list:
            for _group in group_list:
                column_id_set.add(convert_column[_group]['column_id'])
        if aggregate:
            for _aggregate in aggregate.keys():
                column_id_set.add(convert_column[_aggregate]['column_id'])
        if calc_columns_set:
            for column_id in calc_columns_set:
                column_id_set.add(column_id)

        table = self.join_table
        for column_id in column_id_set:
            if self.column_table[column_id]["ttype"] == model_enums.COLUMN_TTYPE_GROUP:
                self.column_table[column_id]["table"] = table
        return table

    def _get_final_sql_table(self, base_table, group_by_select, group_by, group_exps, conditions, column_id, convert_column=None, is_aid=False):
        """
        将所有计算字段中分段查询出， 并进行组合
        :param base_table: 基础table
        :param group_by_select: 聚合字段筛选
        :param group_by: 聚合字段列表
        :param group_exps: 计算字段分段条件
        :param conditions: 筛选条件
        :param column_id: 计算字段ID
        :param convert_column: 字段映射
        :param is_aid: 是否偏移
        :return: 查询表
        """
        tables = deque()

        origin_table = base_table.select(*group_by_select, group_by=group_by)
        if conditions:
            origin_table.where = conditions

        for index, expression in enumerate(group_exps):
            column_name = f"{self._get_column_column(column_id)}_{index}"

            if expression.select is None:
                column = AGG_OPERATION_DICT["Count"](Literal(1)).as_(column_name)
            else:
                table = self._get_column_table(expression.select.column_id, expression.select.dtype, is_aid)
                column = self._get_column_column(expression.select.column_id, expression.select.dtype, is_aid=is_aid)
                column = AGG_OPERATION_DICT[expression.ttype](getattr(table, column)).as_(column_name)

            table = base_table.select(column, *group_by_select, group_by=group_by)

            calc_part_conditions = self._get_calc_part_conditions(expression.part, convert_column, is_aid)
            conditions_list = []
            if calc_part_conditions:
                conditions_list.append(calc_part_conditions)
            if conditions:
                conditions_list.append(conditions)
            where_obj = And(conditions_list)

            table.where = where_obj

            if "exp" not in self.column_table[column_id]:
                self.column_table[column_id]["exp"] = []
            self.column_table[column_id]["exp"].append({
                "aggregate": expression,
                "table": table,
                "column": column_name,
            })

            tables.append(table)

        left_join_table = origin_table
        while tables:
            right_join_table = tables.popleft()
            join_conditions = list()
            for group_select in group_by_select:
                column_name = group_select.output_name
                join_conditions.append(getattr(origin_table, column_name) == getattr(right_join_table, column_name))
            left_join_table = left_join_table.join(right_join_table, type_="left", condition=And(join_conditions))
        return origin_table, left_join_table

    async def aggregate(self, filters, group_list, aggregate_list, convert_column, is_aid):
        '''
        没有分组字段的聚合操作
        :param filters: 筛选条件
        :param group_list: 聚合字段列表
        :param aggregate_list: 计算方式
        :param convert_column: 转换列表
        :param is_aid: 偏移字段
        :return: kylin查询到的数据
        '''
        base_sql_table = self._get_base_sql_table(
            convert_column=convert_column,
            filters=filters,
            group_list=group_list,
            aggregate=aggregate_list,
            is_aid=is_aid
        )
        group_by = self._get_group_by(group_list, convert_column, is_aid)
        group_by_select_list = self._get_group_by_select_list(group_list, convert_column, is_aid)
        select_list = self._get_select_list(aggregate_list, convert_column, is_aid)
        conditions = self._get_conditions(filters, convert_column, is_aid)

        select = base_sql_table.select(*(select_list + group_by_select_list), group_by=group_by)
        if conditions:
            select.where = conditions
        return self.kylin.execute(select)

    async def aggregate_calc(self, filters, group_list, agg_fields, convert_column, is_aid):
        '''
        带有计算字段的查询
        :param group:
        :param filters: 筛选条件
        :param group_list: 聚合字段列表
        :param agg_fields: 计算字段id
        :param convert_column: 转换列表
        :param is_aid: 偏移字段
        :return: kylin查询到的数据
        '''
        parser = self.column_table[convert_column[agg_fields]["column_id"]]["parser"]

        base_sql_table = self._get_base_sql_table(
            convert_column=convert_column,
            filters=filters,
            group_list=group_list,
            calc_columns_set=parser.column_set,
            is_aid=is_aid
        )

        group_by = self._get_group_by(group_list, convert_column, is_aid)
        group_by_select_list = self._get_group_by_select_list(group_list, convert_column, is_aid)
        conditions = self._get_conditions(filters, convert_column, is_aid)

        base_sql_table, final_sql_table = self._get_final_sql_table(
            base_sql_table,
            group_by_select_list,
            group_by,
            parser.group_exps,
            conditions,
            convert_column[agg_fields]["column_id"],
            convert_column,
            is_aid
        )
        conditions_exps = self._calc_aggregate_select_list(parser.result, convert_column[agg_fields]["column_id"])

        new_group_by_select_list = [getattr(base_sql_table, getattr(group_by_select, "output_name")) for group_by_select in group_by_select_list]
        select = final_sql_table.select(conditions_exps.as_(agg_fields), *new_group_by_select_list)
        return self.kylin.execute(select)
