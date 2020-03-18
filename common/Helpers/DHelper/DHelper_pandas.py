    # encoding=utf8

import os
import datetime
import string
import itertools
import math
import base64
import numpy as np
import pandas as pd
import settings
from apps.errors import AppResourceError
from exceptions import ResourceError
from commons import df_utils
from commons import log_utils
from commons.Helpers.Helper_validate import Validate, RegType
from commons.DHelper.DHelper_base import DHelper_base
from apps.bi import model_enums
from rpc.user.base_client import get_grouplevel

logger = log_utils.get_logging(name='model', file_name='model.log')

NORMAL_DATAFRAME = 1
SPECIAL_DATAFRAME = 2


def get_project_region_dataframe(project_id):
    path = os.path.join(settings.DATA_FILE_PATH, f"region_{project_id}.h5")
    return df_utils.get_dataframe_by_file(path)


def get_aggfunc_by_name(name):
    AGGFUNC_DICT = {
        model_enums.FIELD_AGG_TYPE_COUNT: np.size,
        model_enums.FIELD_AGG_TYPE_NUNIQ: pd.Series.nunique,
        model_enums.FIELD_AGG_TYPE_SUM: np.sum,
        model_enums.FIELD_AGG_TYPE_MEAN: np.mean,
        model_enums.FIELD_AGG_TYPE_MEDIAN: np.median,
        model_enums.FIELD_AGG_TYPE_MAX: np.max,
        model_enums.FIELD_AGG_TYPE_MIN: np.min,
    }

    return AGGFUNC_DICT.get(name)


class DHelper_pandas(DHelper_base):
    """
    pandas版本得数据控制类，包含三大步骤类型
    add_xxx 类方法（主要继承自基类）主要为当前处理类构建环境
    do_xxx 类方法，主要根据当前环境处理数据
    get_xxx 类方法，主要以特定格式输出数据
    """
    def __init__(self, **kwargs):
        if kwargs.get("df") is not None:
            super(DHelper_pandas, self).__init__(kwargs.get("df"))
            self._has_aid = None
            self._has_add_aid_df = False
            self.pivot_df = None
            self.aid_df = None
            self.region_filter_list = []
            self.init_df(kwargs.get("df"))

    def init_df(self, df):
        self.df = df

    def get_conditions(self, check_list, condition="all"):
        total_check_df = None
        while check_list:
            try:
                check_df = check_list.pop()
                if check_df is None:
                    continue
                if isinstance(total_check_df, (pd.DataFrame, pd.Series)):
                    if condition == "all":
                        total_check_df = total_check_df & check_df
                    else:
                        total_check_df = total_check_df | check_df
                else:
                    total_check_df = check_df
            except Exception:
                pass

        return total_check_df

    def _get_series(self, df, pivot):
        def get_sorted_series(agg_series, index_list):
            return agg_series.rank(ascending=pivot.sortfunc, method="min")

        def get_series(df, pivot, index_list):
            grouped_dataframe = df.dropna(subset=[pivot.new_column]).groupby(index_list, observed=True)
            if pivot.aggable:
                agg_series = grouped_dataframe.agg({pivot.new_column: get_aggfunc_by_name(pivot.func)})[pivot.new_column]
            else:
                def test_func(df, result):
                    if len(df) > 0:
                        for step in result.steps:
                            try:
                                df[step[0]] = eval(step[1])
                            except Exception as e:
                                break
                        try:
                            return eval(str(result.result))
                        except Exception:
                            return np.nan

                agg_series = grouped_dataframe.apply(lambda df: test_func(df, pivot.func))
                agg_series.name = pivot.new_column
                
            # sortfunc = True 从小到大
            # sortfunc = False 从大到小
            # 如果要转换为排序
            if pivot.sortfunc is not None:
                agg_series = get_sorted_series(agg_series, index_list)
            return agg_series

        for region_filter in self.region_filter_list:
            if region_filter.new_column == pivot.new_column:
                index_list = pivot.index_list[:] + [region_filter.column]
                output_series = get_series(df, pivot, index_list)
                output_df = pd.DataFrame(output_series).reset_index()
                agg_series = output_df[output_df[region_filter.column].isin(region_filter.value_list)].set_index(pivot.index_list)[pivot.new_column]
                return agg_series

        agg_series = get_series(df, pivot, pivot.index_list)
        return agg_series

    def _get_serie_data(self, pivot):
        if self._has_aid_df() and pivot.multifunc == model_enums.FIELD_MULTI_AGG_TYPE_CHAIN_RATIO:
            series = self._get_series(self.df, pivot)
            serie_tmp = self._get_series(self.aid_df, pivot)
            df_tmp = pd.DataFrame([series, serie_tmp], index=[0, 1]).T.dropna()
            df_tmp[pivot.new_column] = ((1.0 * df_tmp.iloc[:, 0] / df_tmp.iloc[:, 1]) - 1) * 100
            return df_tmp[pivot.new_column]
        elif self._has_aid_df() and pivot.multifunc == model_enums.FIELD_MULTI_AGG_TYPE_CHAIN_CHANGE:
            series = self._get_series(self.df, pivot)
            serie_tmp = self._get_series(self.aid_df, pivot)
            df_tmp = pd.DataFrame([series, serie_tmp], index=[0, 1]).T.dropna()
            df_tmp[pivot.new_column] = df_tmp.iloc[:, 0] - df_tmp.iloc[:, 1]
            return df_tmp[pivot.new_column]
        elif pivot.multifunc == model_enums.FIELD_MULTI_AGG_TYPE_PERCENT:
            series = self._get_series(self.df, pivot)
            df_tmp = pd.DataFrame([series], index=[0]).T.dropna()
            df_tmp[pivot.new_column] = df_tmp.iloc[:, 0] / df_tmp.iloc[:, 0].sum()
            return df_tmp[pivot.new_column]
        else:
            return self._get_series(self.df, pivot)

    def _has_aid_df(self):
        if self._has_aid is None:
            self._has_aid = True
            for new_column in self._new_column_list:
                if new_column.dtype in (
                        model_enums.FIELD_DTYPE_DATETIME,
                ):
                    self._get_aid_tmp_datetime(new_column.date_type)
                    break
            else:
                self._has_aid = False
                return self._has_aid

            for new_column in self._new_column_list:
                if new_column.multifunc in (
                        model_enums.FIELD_MULTI_AGG_TYPE_CHAIN_RATIO,
                        model_enums.FIELD_MULTI_AGG_TYPE_CHAIN_CHANGE,
                ):
                    break
            else:
                self._has_aid = False
                return self._has_aid
        return self._has_aid

    def _do_add_aid_df(self, df):
        self.aid_df = df.copy()

    def _get_aid_tmp_datetime(self, date_group):
        if date_group == model_enums.FIELD_DTYPE_DATETIME_Y:
            self.tmp_datetime = datetime.timedelta(days=-366)
        elif date_group == model_enums.FIELD_DTYPE_DATETIME_Q:
            self.tmp_datetime = datetime.timedelta(days=-93)
        elif date_group == model_enums.FIELD_DTYPE_DATETIME_M:
            self.tmp_datetime = datetime.timedelta(days=-31)
        elif date_group == model_enums.FIELD_DTYPE_DATETIME_W:
            self.tmp_datetime = datetime.timedelta(days=-7)
        elif date_group == model_enums.FIELD_DTYPE_DATETIME_D:
            self.tmp_datetime = datetime.timedelta(days=-1)

    def _do_aid_filter(self):
        condition_list = []
        for filter_item in self._filter_list:
            if filter_item.option == "in":
                if isinstance(filter_item.value, list):
                    condition = (self.aid_df[filter_item.column].isin(filter_item.value))
                else:
                    condition = (self.aid_df[filter_item.column].isin([filter_item.value]))
            elif filter_item.option == "notin":
                if isinstance(filter_item.value, list):
                    condition = (~self.aid_df[filter_item.column].isin(filter_item.value))
                else:
                    condition = (~self.aid_df[filter_item.column].isin([filter_item.value]))
            elif filter_item.option == "contain":
                condition = (self.aid_df[filter_item.column].str.contains(filter_item.value))
            elif filter_item.option == "notcontain":
                condition = (~self.aid_df[filter_item.column].str.contains(filter_item.value))
            elif filter_item.option == "empty":
                condition = (self.aid_df[filter_item.column].isnull())
            elif filter_item.option == "notempty":
                condition = (self.aid_df[filter_item.column].notnull())
            elif filter_item.option == "gt":
                condition = (self.aid_df[filter_item.column] > filter_item.value)
            elif filter_item.option == "lt":
                condition = (self.aid_df[filter_item.column] < filter_item.value)
            elif filter_item.option == "gte":
                condition = (self.aid_df[filter_item.column] >= filter_item.value)
            elif filter_item.option == "lte":
                condition = (self.aid_df[filter_item.column] <= filter_item.value)
            elif filter_item.option == "eq":
                condition = (self.aid_df[filter_item.column] == filter_item.value)
            elif filter_item.option == "ne":
                condition = (self.aid_df[filter_item.column] != filter_item.value)
            elif filter_item.option is None:
                if filter_item.value:
                    if isinstance(filter_item.value, list):
                        condition = (self.aid_df[filter_item.column].isin(filter_item.value))
                    else:
                        condition = (self.aid_df[filter_item.column].isin([filter_item.value]))
                else:
                    condition = None
            else:
                condition = None
            condition_list.append(condition)

        conditions = self.get_conditions(condition_list)
        if conditions is not None:
            self.aid_df = self.aid_df[conditions]

    def _do_aid_add_new_column(self):
        for new_column in self._new_column_list:
            if self.aid_df.empty:
                raise ResourceError(AppResourceError.NoData, "数据为空!")

            if new_column.column_ttype == model_enums.COLUMN_TTYPE_CALC:
                self.aid_df[new_column.new_column] = 0.0
            else:
                if new_column.dtype == model_enums.FIELD_DTYPE_DATETIME:
                    if new_column.date_type == model_enums.FIELD_DATE_TYPE_YEAR:
                        self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_year"]
                    elif new_column.date_type == model_enums.FIELD_DATE_TYPE_QUARTER:
                        self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_quarter"]
                    elif new_column.date_type == model_enums.FIELD_DATE_TYPE_MONTH:
                        self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_month"]
                    elif new_column.date_type == model_enums.FIELD_DATE_TYPE_WEEK:
                        self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_week"]
                    elif new_column.date_type == model_enums.FIELD_DATE_TYPE_DAY:
                        self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_day"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_Y:
                    self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_y"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_Q:
                    self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_q"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_M:
                    self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_m"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_W:
                    self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_w"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_WD:
                    self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_wd"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_D:
                    self.aid_df[new_column.new_column] = self.aid_df[f"{new_column.column}_aid_d"]
                else:
                    self.aid_df[new_column.new_column] = self.aid_df[new_column.column]

    def _do_aid_drilldown(self):
        for drilldown in self._drilldown_list:
            self.aid_df = self.aid_df[self.aid_df[drilldown.new_column] == drilldown.value]

    def _do_aid_field_filter(self):
        for field_filter in self._field_filter_list:
            if self.aid_df.empty:
                self.aid_df[field_filter.new_column] = np.nan
            else:
                if field_filter.sort:
                    self.region_filter_list.append(field_filter)
                    # TODO 这里添加顶点层级筛选， 后续直接排序后做筛选即可, 下面的两句赋值需要修改
                    sort_column = field_filter.column
                    sort_value_list = field_filter.value_list
                    self.df[field_filter.new_column] = self.df[self.df[sort_column].isin(sort_value_list)][field_filter.new_column]
                else:
                    self.aid_df[field_filter.new_column] = self.aid_df[self.aid_df[field_filter.column].isin(field_filter.value_list)][field_filter.new_column]

    def _do_filter(self):
        condition_list = []
        for filter_item in self._filter_list:
            if filter_item.option == "in":
                if isinstance(filter_item.value, list):
                    condition = (self.df[filter_item.column].isin(filter_item.value))
                else:
                    condition = (self.df[filter_item.column].isin([filter_item.value]))
            elif filter_item.option == "notin":
                if isinstance(filter_item.value, list):
                    condition = (~self.df[filter_item.column].isin(filter_item.value))
                else:
                    condition = (~self.df[filter_item.column].isin([filter_item.value]))
            elif filter_item.option == "contain":
                condition = (self.df[filter_item.column].str.contains(filter_item.value))
            elif filter_item.option == "notcontain":
                condition = (~self.df[filter_item.column].str.contains(filter_item.value))
            elif filter_item.option == "empty":
                condition = (self.df[filter_item.column].isnull())
            elif filter_item.option == "notempty":
                condition = (self.df[filter_item.column].notnull())
            elif filter_item.option == "gt":
                condition = (self.df[filter_item.column] > filter_item.value)
            elif filter_item.option == "lt":
                condition = (self.df[filter_item.column] < filter_item.value)
            elif filter_item.option == "gte":
                condition = (self.df[filter_item.column] >= filter_item.value)
            elif filter_item.option == "lte":
                condition = (self.df[filter_item.column] <= filter_item.value)
            elif filter_item.option == "eq":
                condition = (self.df[filter_item.column] == filter_item.value)
            elif filter_item.option == "ne":
                condition = (self.df[filter_item.column] != filter_item.value)
            elif filter_item.option is None:
                if filter_item.value:
                    if isinstance(filter_item.value, list):
                        condition = (self.df[filter_item.column].isin(filter_item.value))
                    else:
                        condition = (self.df[filter_item.column].isin([filter_item.value]))
                else:
                    condition = None
            else:
                condition = None
            condition_list.append(condition)

        conditions = self.get_conditions(condition_list)
        if conditions is not None:
            self.df = self.df[conditions]

    def _do_add_new_column(self):
        for new_column in self._new_column_list:
            if self.df.empty:
                raise ResourceError(AppResourceError.NoData, "数据为空!")

            if new_column.column_ttype == model_enums.COLUMN_TTYPE_CALC:
                self.df[new_column.new_column] = 0.0
            else:
                if new_column.dtype == model_enums.FIELD_DTYPE_DATETIME:
                    if new_column.date_type == model_enums.FIELD_DATE_TYPE_YEAR:
                        self.df[new_column.new_column] = self.df[f"{new_column.column}_year"]
                    elif new_column.date_type == model_enums.FIELD_DATE_TYPE_QUARTER:
                        self.df[new_column.new_column] = self.df[f"{new_column.column}_quarter"]
                    elif new_column.date_type == model_enums.FIELD_DATE_TYPE_MONTH:
                        self.df[new_column.new_column] = self.df[f"{new_column.column}_month"]
                    elif new_column.date_type == model_enums.FIELD_DATE_TYPE_WEEK:
                        self.df[new_column.new_column] = self.df[f"{new_column.column}_week"]
                    elif new_column.date_type == model_enums.FIELD_DATE_TYPE_DAY:
                        self.df[new_column.new_column] = self.df[f"{new_column.column}_day"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_Y:
                    self.df[new_column.new_column] = self.df[f"{new_column.column}_y"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_Q:
                    self.df[new_column.new_column] = self.df[f"{new_column.column}_q"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_M:
                    self.df[new_column.new_column] = self.df[f"{new_column.column}_m"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_W:
                    self.df[new_column.new_column] = self.df[f"{new_column.column}_w"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_WD:
                    self.df[new_column.new_column] = self.df[f"{new_column.column}_wd"]
                elif new_column.dtype == model_enums.FIELD_DTYPE_DATETIME_D:
                    self.df[new_column.new_column] = self.df[f"{new_column.column}_d"]
                else:
                    self.df[new_column.new_column] = self.df[new_column.column]

    def _do_drilldown(self):
        for drilldown in self._drilldown_list:
            if isinstance(drilldown.value, (list, )):
                self.df = self.df[self.df[str(drilldown.new_column)].isin(drilldown.value)]
            else:
                self.df = self.df[self.df[str(drilldown.new_column)] == drilldown.value]

    def _do_field_filter(self):
        for field_filter in self._field_filter_list:
            if self.df.empty:
                self.df[field_filter.new_column] = np.nan
            else:
                if field_filter.sort:
                    self.region_filter_list.append(field_filter)
                    # TODO 这里添加顶点层级筛选， 后续直接排序后做筛选即可, 下面的两句赋值需要修改
                    sort_column = field_filter.column
                    sort_value_list = field_filter.value_list
                    self.df[field_filter.new_column] = self.df[self.df[sort_column].isin(sort_value_list)][field_filter.new_column]
                else:
                    self.df[field_filter.new_column] = self.df[self.df[field_filter.column].isin(field_filter.value_list)][field_filter.new_column]

    def do_preprocess(self):
        if self._has_aid_df() and not self._has_add_aid_df:
            # 创建一个时间经过偏移的拷贝
            self._do_add_aid_df(self.df)
            # 所有操作作用在一个偏移了时间的拷贝上
            self._do_aid_filter()
            self._do_aid_add_new_column()
            self._do_aid_drilldown()
            self._do_aid_field_filter()
            self._has_add_aid_df = True

        # 数据预处理， 所有操作直接作用在self.df上
        self._do_filter()
        self._do_add_new_column()
        self._do_drilldown()
        self._do_field_filter()

        # [swxs] TODO: 下列信息不删掉可能有很大用处
        self._filter_list = []
        self._new_column_list = []
        self._drilldown_list = []
        self._field_filter_list = []
        return self.df

    def _get_main_df(self, pivot_list, has_colortag, fillna=settings.NONE_DATA):
        main_serie_list = []
        for pivot in pivot_list:
            serie = self._get_serie_data(pivot).dropna()
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

        def get_field_name(df, column):
            return f"{df.index[0]}\001{get_column_name(column)}"

        def get_split_colortag_df(base_df):
            all_data = base_df.values[0].tolist()
            if hasattr(base_df.columns, "levels"):
                # 非对比列所有可选项
                new_columns = list()
                for column in base_df.columns.droplevel(level=-1).tolist():
                    if column not in new_columns:
                        new_columns.append(column)

                # 将非对比列所有情况映射到各个对比列选项字典中
                new_columns_names = base_df.columns.names[:-1]
                data_dict = dict()
                for i, data in enumerate(all_data):
                    field_name = get_field_name(base_df, base_df.columns[i][-1])
                    if field_name not in data_dict:
                        data_dict[field_name] = dict()
                    data_dict[field_name][get_column_name(base_df.columns[i][0:-1])] = data
                if len(new_columns_names) == 1:
                    part_df = pd.DataFrame(data_dict, index=pd.Index(new_columns)).T
                else:
                    #  https://github.com/pandas-dev/pandas/issues/12457
                    part_df = pd.DataFrame(data_dict, index=pd.MultiIndex.from_tuples(new_columns)).T
            else:
                # 对比列所有可选项
                new_columns = [settings.COLUMN_ALL]

                # 将非对比列所有情况映射到各个对比列选项字典中
                new_columns_names = [settings.COLUMN_ALL]
                colortag_columns = base_df.columns.tolist()
                data_dict = dict()
                for columns in colortag_columns:
                    data_dict[get_field_name(base_df, columns)] = list()
                for columns in colortag_columns:
                    data_dict[get_field_name(base_df, columns)] = [np.nan]
                for i, data in enumerate(all_data):
                    data_dict[get_field_name(base_df, colortag_columns[i])] = [data]
                part_df = pd.DataFrame(data_dict, index=new_columns).T
            part_df.columns.set_names(new_columns_names, inplace=True)
            return part_df

        if has_colortag and len(pivot_list) > 0:  # 存在对比
            all_df = pd.DataFrame()
            for index, series in tmp_df.iterrows():
                all_df = all_df.append(get_split_colortag_df(pd.DataFrame(series).T))
            tmp_df = all_df
        # [swxs] TODO: 下列信息不删掉可能有很大用处
        pivot_list = []
        return tmp_df

    def _get_sub_df(self, pivot_list, has_colortag, fillna=settings.NONE_DATA):
        sub_serie_list = []
        for pivot in pivot_list:
            serie = self._get_serie_data(pivot).dropna()
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
            self._get_main_df(self._pivot_main_list, has_color_tag, fillna=fillna),
            self._get_sub_df(self._pivot_sub_list, has_color_tag, fillna=fillna)
        ], sort=False).fillna(value=fillna)

        self.pivot_x_df = self._get_main_df(self._pivot_main_x_list, has_color_tag, fillna=fillna)
        self.pivot_y_df = self._get_main_df(self._pivot_main_y_list, has_color_tag, fillna=fillna)

        self.group_df = pd.concat([
            self.pivot_x_df,
            self.pivot_y_df,
            self._get_sub_df(self._pivot_sub_list, has_color_tag, fillna=fillna)
        ]).fillna(value=fillna)

        self._pivot_main_list = []
        self._pivot_sub_list = []
        self._pivot_main_x_list = []
        self._pivot_main_y_list = []
        return self.pivot_df, self.pivot_x_df, self.pivot_y_df

    def do_rank(self, d_type, ascending, sort_index, x_axis_count=None, dropna=settings.NONE_DATA):
        if d_type == 1:
            if len(self.pivot_df) > 0:
                self.pivot_df = self.pivot_df.T[~self.pivot_df.T.iloc[:, sort_index].isin([dropna])].T
                ranked_series = self.pivot_df.iloc[sort_index].rank()
                ranked_index = ranked_series.sort_values('index', ascending=ascending).index
                self.pivot_df = self.pivot_df.T.reindex(ranked_index).T
                if x_axis_count:
                    self.pivot_df = self.pivot_df.iloc[:, 0:x_axis_count]
        elif d_type == 2:
            if len(self.pivot_df.T) > 0:
                self.pivot_df = self.pivot_df[~self.pivot_df.iloc[:, 0].isin([dropna])]
                ranked_series = self.pivot_df.rank().iloc[:, 0]
                ranked_index = ranked_series.sort_values('index', ascending=ascending).index
                self.pivot_df = self.pivot_df.reindex(ranked_index)
                if x_axis_count:
                    self.pivot_df = self.pivot_df.iloc[0:x_axis_count, :]
        return self.pivot_df

    def do_refresh(self, field_id_list):
        df_columns = self.df.columns.tolist()
        field_id_list = [field_id for field_id in field_id_list if field_id in df_columns]
        self.df.drop(labels=field_id_list, axis=1, inplace=True)

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
        index_range = slice(*(slice(start, end).indices(len(self.df))))
        return self.df.iloc[index_range, :]

    def get_field_unique_value_list(self, column, dtype=None):
        """
        在获取筛选可选项及钻取可选项列表时需要获取所有可选项值
        :param column_name:
        :param dtype:
        :return:
        """
        #  面对极限的筛选条件可能出现对应列不存在的情况？ column_name 会莫名丢失？
        if column.col not in self.df.columns.tolist():
            logger.debug(f"column: {column.col} not in {self.df.columns.tolist()}!")
            return []

        if dtype == model_enums.FIELD_DTYPE_DATETIME_Y:
            return self.df[f"{column.col}_y"].unique().tolist()
        elif dtype == model_enums.FIELD_DTYPE_DATETIME_Q:
            return self.df[f"{column.col}_q"].unique().tolist()
        elif dtype == model_enums.FIELD_DTYPE_DATETIME_M:
            return self.df[f"{column.col}_m"].unique().tolist()
        elif dtype == model_enums.FIELD_DTYPE_DATETIME_W:
            return self.df[f"{column.col}_w"].unique().tolist()
        elif dtype == model_enums.FIELD_DTYPE_DATETIME_WD:
            return self.df[f"{column.col}_wd"].unique().tolist()
        elif dtype == model_enums.FIELD_DTYPE_DATETIME_D:
            return self.df[f"{column.col}_d"].unique().tolist()
        else:
            return self.df[column.col].unique().tolist()
