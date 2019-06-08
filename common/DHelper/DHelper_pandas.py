# encoding=utf8

import os
import datetime
import numpy as np
import pandas as pd
import settings
from api.consts.bi import field as field_consts
from api.utils.bi.field import Field
from api.utils.organization.region_type import RegionType
from common.Exceptions import NoDataException
from common.Utils import df_utils
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_validate import Validate, RegType
from common.Utils.DateUtils import date_range
from common.DHelper.DHelper_base import DHelper_base

log = getLogger('DHelper_pandas.py')

NORMAL_DATAFRAME = 1
SPECIAL_DATAFRAME = 2


def get_project_region_dataframe(project_id):
    path = os.path.join(settings.DATA_FILE_PATH, f"region_{project_id}.h5")
    return df_utils.get_dataframe_by_file(path)

class DHelper_pandas(DHelper_base):
    def __new__(cls, *args, **kwargs):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.__singleton__ = singleton = object.__new__(cls)
        return singleton

    def __init__(self, df=None, project_id=None):
        if df is not None:
            super(DHelper_pandas, self).__init__(df)
            self.project_id = project_id

            self._has_aid = None
            self._has_add_aid_df = False
            self.pivot_df = None
            self.aid_df = None
            self.region_filter_list = []
            self.init_df(df)

    def init_df(self, df):
        self.df = df

    def _get_series(self, df, pivot):
        def get_index(series, ranked_index_list):
            i, j = 1, None
            output_list = []
            for index, rank_index in enumerate(ranked_index_list, 1):
                if j is None:
                    output_list.append(i)
                    j = series[rank_index]
                else:
                    if j == series[rank_index]:
                        output_list.append(i)
                    else:
                        i = index
                        j = series[rank_index]
                        output_list.append(i)
            return output_list

        def get_series(df, pivot, index_list):
            grouped_dataframe = df.dropna(subset=[pivot.new_column]).groupby(index_list)
            if pivot.aggable:
                agg_series = grouped_dataframe.agg({pivot.new_column: field_consts.get_aggfunc_by_name(pivot.func)})[pivot.new_column]
            else:
                def test_func(df, func):
                    if len(df) > 0:
                        try:
                            return eval(func)
                        except:
                            return np.nan

                agg_series = grouped_dataframe.apply(lambda df: test_func(df, pivot.func))
                agg_series.name = pivot.new_column

            # sortfunc = True 从小到大
            # sortfunc = False 从大到小
            # 如果要转换为排序
            if pivot.sortfunc is not None:
                left_field_id = None  # 合表的列名， 如果是使用维度字段， 则是field_id, 否则为层级中的一个层级名
                right_field_id = None  # 合表的列名， 层级名
                region_column_list = []  # 只需要导入下列字段

                min_region_type = None  # 最小的层级名
                min_field_id = None  # 最小层级对应的field_id (使用维度情况下)
                current_level = 0  # 记录当前层级， 最高层做特殊处理（level==0时， 使用无层级处理的模式处理）
                for field_id in index_list:  # index_list， 只有维度情况下只包含维度（对比），在数据范围模式下包含了数据范围对应的层级名
                    if Validate.check(field_id, reg_type=RegType.COLUMN_ID):
                        region_type_display_name = Field.get_field_by_field_id(field_id).column
                        current_region_type = RegionType.get_region_type_by_display_name_project_id(region_type_display_name, self.project_id)
                    else:
                        current_region_type = RegionType.get_region_type_by_display_name_project_id(field_id, self.project_id)
                    # 到这里 region_type 是对应的层级， field_id 是 表中的列名

                    if (current_region_type is not None) and (current_region_type.level > current_level):
                        min_region_type = current_region_type  # 当前最小的层级
                        min_field_id = field_id  # 最小层级所对应的列名
                        current_level = current_region_type.level  # 当前层级

                if min_region_type is not None:
                    left_field_id = min_field_id
                    right_field_id = min_region_type.display_name
                    for region_type in RegionType.get_region_type_list_by_project_id(self.project_id):
                        if 0 < region_type.level <= min_region_type.level:
                            region_column_list.append(region_type.display_name)

                if pivot.sort_regiontype_id is not None:  # 如果是要查看在全国内的排名， 则使用（level==0时， 使用无层级处理的模式处理）
                    region_type = RegionType.get_region_type_by_id(pivot.sort_regiontype_id)
                    if region_type.level == 0:
                        left_field_id = None

                if (left_field_id is None) or (pivot.sort_regiontype_id is None):
                    ranked_index = agg_series.rank(ascending=True).sort_values('index', ascending=pivot.sortfunc).index
                    ranked_index_list = ranked_index.values.tolist()
                    agg_series = pd.Series(get_index(agg_series, ranked_index_list), name=agg_series.name, index=ranked_index)
                else:
                    sort_region_type = RegionType.get_region_type_by_id(pivot.sort_regiontype_id)

                    output_series_name = agg_series.name
                    output_series_index = agg_series.index

                    #  这里获取层级结构表中指定的层级并去重， 否则数据行数会增加
                    region_base_df = get_project_region_dataframe(self.project_id)
                    region_df = region_base_df[region_column_list].drop_duplicates()
                    df_from_series = pd.DataFrame(agg_series).reset_index()
                    df_with_region = pd.merge(left=df_from_series, right=region_df, left_on=left_field_id, right_on=right_field_id, how="left")
                    # df_with_region = pd.merge(left=df_from_series, right=region_df, left_on=left_field_id, right_on=right_field_id, how="left").groupby([left_field_id]).mean().reset_index()
                    df_with_region.columns.tolist()

                    # 到这里要计算指定层级下每个子层级的排名， 并组合
                    grouped_with_region_df = df_with_region.groupby([sort_region_type.display_name])
                    reseted_index_series = pd.Series()
                    for index, df in grouped_with_region_df:
                        ranked_index = df[output_series_name].rank(ascending=True).sort_values('index', ascending=pivot.sortfunc).index
                        ranked_index_list = ranked_index.values.tolist()
                        reseted_index_series = reseted_index_series.append(pd.Series(get_index(df[output_series_name], ranked_index_list), name="tmp", index=ranked_index))
                    df_with_region[output_series_name] = reseted_index_series
                    agg_series = df_with_region.set_index(index_list)[output_series_name]
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
        if self._has_aid_df() and pivot.multifunc == field_consts.MULTIFUNC_CHAIN_RATIO:
            series = self._get_series(self.df, pivot)
            serie_tmp = self._get_series(self.aid_df, pivot)
            df_tmp = pd.DataFrame([series, serie_tmp], index=[0, 1]).T.dropna()
            df_tmp[pivot.new_column] = ((1.0 * df_tmp.iloc[:, 0] / df_tmp.iloc[:, 1]) - 1) * 100
            return df_tmp[pivot.new_column]
        elif self._has_aid_df() and pivot.multifunc == field_consts.MULTIFUNC_CHAIN_CHANGE:
            series = self._get_series(self.df, pivot)
            serie_tmp = self._get_series(self.aid_df, pivot)
            df_tmp = pd.DataFrame([series, serie_tmp], index=[0, 1]).T.dropna()
            df_tmp[pivot.new_column] = df_tmp.iloc[:, 0] - df_tmp.iloc[:, 1]
            return df_tmp[pivot.new_column]
        else:
            return self._get_series(self.df, pivot)

    def _has_aid_df(self):
        if self._has_aid is None:
            self._has_aid = True
            self._aid_datagroup = None
            for new_column in self._new_column_list:
                if new_column.dtype in [field_consts.DTYPE_DATETIME, ]:
                    self._aid_datagroup = new_column.dategroup
                    break
            else:
                for filter in self._filter_list:
                    if filter.dtype in [field_consts.DTYPE_DATETIME_Y, field_consts.DTYPE_DATETIME_Q,
                                        field_consts.DTYPE_DATETIME_M, field_consts.DTYPE_DATETIME_W,
                                        field_consts.DTYPE_DATETIME_WD, field_consts.DTYPE_DATETIME_D]:
                        break
                else:
                    self._has_aid = False
                    return self._has_aid

            for new_column in self._new_column_list:
                if new_column.multifunc in [field_consts.MULTIFUNC_CHAIN_RATIO, field_consts.MULTIFUNC_CHAIN_CHANGE]:
                    break
            else:
                self._has_aid = False
                return self._has_aid
        return self._has_aid

    def _get_aid_tmp_datetime(self):
        if self._aid_datagroup == field_consts.DATEGROUP_YEAR:
            self.tmp_datetime = datetime.timedelta(days=-366)
        elif self._aid_datagroup == field_consts.DATEGROUP_QUARTER:
            self.tmp_datetime = datetime.timedelta(days=-93)
        elif self._aid_datagroup == field_consts.DATEGROUP_MONTH:
            self.tmp_datetime = datetime.timedelta(days=-31)
        elif self._aid_datagroup == field_consts.DATEGROUP_WEEK:
            self.tmp_datetime = datetime.timedelta(days=-7)
        elif self._aid_datagroup == field_consts.DATEGROUP_DAY:
            self.tmp_datetime = datetime.timedelta(days=-1)

    def _do_add_aid_df(self, df):
        self.aid_df = df.copy()

    def _do_aid_filter(self):
        for filter in self._filter_list:
            if filter.dtype == field_consts.DTYPE_DATETIME:
                start_time, end_time = filter.value_list
                if start_time:
                    if self.tmp_datetime:
                        start_time = start_time + self.tmp_datetime
                    self.aid_df = self.aid_df[self.aid_df[filter.column] >= start_time]
                if end_time:
                    self.aid_df = self.aid_df[self.aid_df[filter.column] < end_time]
            elif filter.dtype == field_consts.DTYPE_DATETIME_Y:
                self.aid_df = (self.aid_df[self.aid_df[filter.column]
                               .apply(self._change_aid_dtype_datetime_y)
                               .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_Q:
                self.aid_df = (self.aid_df[self.aid_df[filter.column]
                               .apply(self._change_aid_dtype_datetime_q)
                               .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_M:
                self.aid_df = (self.aid_df[self.aid_df[filter.column]
                               .apply(self._change_aid_dtype_datetime_m)
                               .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_W:
                self.aid_df = (self.aid_df[(self.aid_df[filter.column] + pd.Timedelta(1, unit='W'))
                               .apply(self._change_aid_dtype_datetime_w)
                               .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_WD:
                self.aid_df = (self.aid_df[(self.aid_df[filter.column] + pd.Timedelta(1, unit='W'))
                               .apply(self._change_aid_dtype_datetime_wd)
                               .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_D:
                self.aid_df = (self.aid_df[(self.aid_df[filter.column] + pd.Timedelta(1, unit='D'))
                               .apply(self._change_aid_dtype_datetime_d)
                               .isin(filter.value_list)])
            else:
                self.aid_df = self.aid_df[self.aid_df[filter.column].isin(filter.value_list)]

    def _do_aid_add_new_column(self):
        for new_column in self._new_column_list:
            if len(self.aid_df) == 0:
                raise NoDataException()

            if not new_column.aggable:
                self.aid_df[new_column.new_column] = 0.0
            else:
                if new_column.dtype == field_consts.DTYPE_DATETIME:
                    if new_column.dategroup == field_consts.DATEGROUP_YEAR:
                        self.aid_df[new_column.new_column] = self.aid_df[new_column.column].apply(self._change_aid_dategroup_year)
                    elif new_column.dategroup == field_consts.DATEGROUP_QUARTER:
                        self.aid_df[new_column.new_column] = self.aid_df[new_column.column].apply(self._change_aid_dategroup_quarter)
                    elif new_column.dategroup == field_consts.DATEGROUP_MONTH:
                        self.aid_df[new_column.new_column] = self.aid_df[new_column.column].apply(self._change_aid_dategroup_month)
                    elif new_column.dategroup == field_consts.DATEGROUP_WEEK:
                        self.aid_df[new_column.new_column] = (self.aid_df[new_column.column] + pd.Timedelta(1, unit='W')).apply(self._change_aid_dategroup_week)
                    elif new_column.dategroup == field_consts.DATEGROUP_DAY:
                        self.aid_df[new_column.new_column] = (self.aid_df[new_column.column] + pd.Timedelta(1, unit='D')).apply(self._change_aid_dategroup_day)
                elif new_column.dtype == field_consts.DTYPE_DATETIME_Y:
                    self.aid_df[new_column.new_column] = self.aid_df[new_column.column].apply(self._change_aid_dtype_datetime_y)
                elif new_column.dtype == field_consts.DTYPE_DATETIME_Q:
                    self.aid_df[new_column.new_column] = self.aid_df[new_column.column].apply(self._change_aid_dtype_datetime_q)
                elif new_column.dtype == field_consts.DTYPE_DATETIME_M:
                    self.aid_df[new_column.new_column] = self.aid_df[new_column.column].apply(self._change_aid_dtype_datetime_m)
                elif new_column.dtype == field_consts.DTYPE_DATETIME_W:
                    self.aid_df[new_column.new_column] = (self.aid_df[new_column.column] + pd.Timedelta(1, unit='W')).apply(self._change_dtype_datetime_w)
                elif new_column.dtype == field_consts.DTYPE_DATETIME_WD:
                    self.aid_df[new_column.new_column] = (self.aid_df[new_column.column] + pd.Timedelta(1, unit='W')).apply(self._change_dtype_datetime_wd)
                elif new_column.dtype == field_consts.DTYPE_DATETIME_D:
                    self.aid_df[new_column.new_column] = (self.aid_df[new_column.column] + pd.Timedelta(1, unit='D')).apply(self._change_dtype_datetime_d)
                else:
                    self.aid_df[new_column.new_column] = self.aid_df[new_column.column]

    def _do_aid_drilldown(self):
        for drilldown in self._drilldown_list:
            self.aid_df = self.aid_df[self.aid_df[drilldown.new_column] == drilldown.value]

    def _do_aid_field_filter(self):
        for field_filter in self._field_filter_list:
            if len(self.aid_df) == 0:
                self.aid_df[field_filter.new_column] = np.nan
            else:
                self.aid_df[field_filter.new_column] = self.aid_df[self.aid_df[field_filter.column].isin(field_filter.value_list)][field_filter.new_column]

    def _do_filter(self):
        for filter in self._filter_list:
            if filter.dtype == field_consts.DTYPE_DATETIME:
                start_time = filter.value_list[1]
                end_time = filter.value_list[2]
                if start_time:
                    self.df = self.df[self.df[filter.column] >= start_time]
                if end_time:
                    self.df = self.df[self.df[filter.column] < end_time]
            elif filter.dtype == field_consts.DTYPE_DATETIME_Y:
                self.df = (self.df[self.df[filter.column]
                           .apply(self._change_dtype_datetime_y)
                           .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_Q:
                self.df = (self.df[self.df[filter.column]
                           .apply(self._change_dtype_datetime_q)
                           .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_M:
                self.df = (self.df[self.df[filter.column]
                           .apply(self._change_dtype_datetime_m)
                           .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_W:
                self.df = (self.df[self.df[filter.column]
                           .apply(self._change_dtype_datetime_w)
                           .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_WD:
                self.df = (self.df[self.df[filter.column]
                           .apply(self._change_dtype_datetime_wd)
                           .isin(filter.value_list)])
            elif filter.dtype == field_consts.DTYPE_DATETIME_D:
                self.df = (self.df[self.df[filter.column]
                           .apply(self._change_dtype_datetime_d)
                           .isin(filter.value_list)])
            else:
                if filter.column in self.df.columns.tolist():
                    self.df = self.df[self.df[filter.column].isin(filter.value_list)]

    def _do_add_new_column(self):
        for new_column in self._new_column_list:
            if len(self.df) == 0:
                raise NoDataException()

            if not new_column.aggable:
                self.df[new_column.new_column] = 0.0
            else:
                if new_column.dtype == field_consts.DTYPE_DATETIME:
                    if new_column.dategroup == field_consts.DATEGROUP_YEAR:
                        self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dategroup_year))
                    elif new_column.dategroup == field_consts.DATEGROUP_QUARTER:
                        self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dategroup_quarter))
                    elif new_column.dategroup == field_consts.DATEGROUP_MONTH:
                        self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dategroup_month))
                    elif new_column.dategroup == field_consts.DATEGROUP_WEEK:
                        self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dategroup_week))
                    elif new_column.dategroup == field_consts.DATEGROUP_DAY:
                        self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dategroup_day))
                elif new_column.dtype == field_consts.DTYPE_DATETIME_Y:
                    self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dtype_datetime_y))
                elif new_column.dtype == field_consts.DTYPE_DATETIME_Q:
                    self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dtype_datetime_q))
                elif new_column.dtype == field_consts.DTYPE_DATETIME_M:
                    self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dtype_datetime_m))
                elif new_column.dtype == field_consts.DTYPE_DATETIME_W:
                    self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dtype_datetime_w))
                elif new_column.dtype == field_consts.DTYPE_DATETIME_WD:
                    self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dtype_datetime_wd))
                elif new_column.dtype == field_consts.DTYPE_DATETIME_D:
                    self.df[new_column.new_column] = (self.df[new_column.column].apply(self._change_dtype_datetime_d))
                else:
                    self.df[new_column.new_column] = self.df[new_column.column]

    def _do_drilldown(self):
        for drilldown in self._drilldown_list:
            self.df = self.df[self.df[drilldown.new_column] == drilldown.value]

    def _do_field_filter(self):
        for field_filter in self._field_filter_list:
            if len(self.df) == 0:
                self.df[field_filter.new_column] = np.nan
            else:
                if field_filter.sort:
                    self.region_filter_list.append(field_filter)
                else:
                    self.df[field_filter.new_column] = self.df[self.df[field_filter.column].isin(field_filter.value_list)][field_filter.new_column]

    def do_preprocess(self):
        if self._has_aid_df() and not self._has_add_aid_df:
            # 创建一个时间经过偏移的拷贝
            self._get_aid_tmp_datetime()
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

    def _get_main_df(self, has_colortag, fillna=settings.NONE_DATA):
        main_serie_list = []
        for pivot in self._pivot_main_list:
            serie = self._get_serie_data(pivot).dropna()
            main_serie_list.append(serie)

        # tmp_df = pd.DataFrame(main_serie_list)
        if main_serie_list:
            # 经过排序处理之后的各series的index可能不再相同顺序， 导致合并的df缺失columns.name[s], 此处以
            # 第一个series的index作为合并df的column
            tmp_df = pd.DataFrame(main_serie_list, columns=main_serie_list[0].index)
        else:
            tmp_df = pd.DataFrame()

        def get_column_name(column):
            try:
                return float(column)
            except:
                return str(column)

        if has_colortag:  # 存在对比
            all_data = tmp_df.values[0].tolist()
            if hasattr(tmp_df.columns, "levels"):
                new_columns_names = tmp_df.columns.names[:-1]
                new_columns = list()
                for column in tmp_df.columns.droplevel(level=-1).tolist():
                    if column not in new_columns:
                        new_columns.append(column)
                colortag_columns = tmp_df.columns.levels[-1].tolist()
                data_dict = dict()
                for columns in colortag_columns:
                    data_dict[get_column_name(columns)] = list()
                old_type = None
                for i, data in enumerate(all_data):
                    if old_type != tmp_df.columns[i][-2]:
                        for columns in colortag_columns:
                            data_dict[get_column_name(columns)].append(np.nan)
                        old_type = tmp_df.columns[i][-2]
                    data_dict[get_column_name(tmp_df.columns[i][-1])].pop()
                    data_dict[get_column_name(tmp_df.columns[i][-1])].append(data)
                if len(new_columns_names) == 1:
                    tmp_df = pd.DataFrame(data_dict, index=new_columns).T
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
        self._pivot_main_list = []
        return tmp_df

    def _get_sub_df(self, has_colortag, fillna=settings.NONE_DATA):
        sub_serie_list = []
        for pivot in self._pivot_sub_list:
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
        self._pivot_sub_list = []
        return tmp_df

    def do_pivot(self, has_colortag, fillna=settings.NONE_DATA):
        self.pivot_df = pd.concat([
            self._get_main_df(has_colortag, fillna=fillna),
            self._get_sub_df(has_colortag, fillna=fillna)
        ]).fillna(value=fillna)
        return self.pivot_df

    def do_rank(self, dtype, ascending, sortIndex, xAxisCount=None, dropna=settings.NONE_DATA):
        if dtype == 1:
            if len(self.pivot_df) > 0:
                self.pivot_df = self.pivot_df.T[~self.pivot_df.T.iloc[:, sortIndex].isin([dropna])].T
                ranked_series = self.pivot_df.iloc[sortIndex].rank()
                ranked_index = ranked_series.sort_values('index', ascending=ascending).index
                self.pivot_df = self.pivot_df.T.reindex(ranked_index).T
                if xAxisCount:
                    self.pivot_df = self.pivot_df.iloc[:, 0:xAxisCount]
        elif dtype == 2:
            if len(self.pivot_df.T) > 0:
                self.pivot_df = self.pivot_df[~self.pivot_df.iloc[:, 0].isin([dropna])]
                ranked_series = self.pivot_df.rank().iloc[:, 0]
                ranked_index = ranked_series.sort_values('index', ascending=ascending).index
                self.pivot_df = self.pivot_df.reindex(ranked_index)
                if xAxisCount:
                    self.pivot_df = self.pivot_df.iloc[0:xAxisCount, :]
        return self.pivot_df

    def do_refresh(self, field_id_list):
        df_columns = self.df.columns.tolist()
        field_id_list = [field_id for field_id in field_id_list if field_id in df_columns]
        self.df.drop(labels=field_id_list, axis=1, inplace=True)

    def _get_head_name(self):
        if self.pivot_df.columns.name:
            return [self.pivot_df.columns.name]
        else:
            return self.pivot_df.columns.names

    def _get_head_value(self):
        return self.pivot_df.columns.tolist()

    def _get_data_list(self, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(self.pivot_df))))
        return [dict(name=field_name, value=self.pivot_df.loc[field_name].tolist())
                for field_name in self.pivot_df.iloc[index_range].index.tolist()]

    def get_base_data(self, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(self.df))))
        return self.df.iloc[index_range, :]

    def get_pivot_data(self, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(self.pivot_df))))
        return self.pivot_df.iloc[index_range, :]

    def get_pivot_data_result(self, start=0, end=None):
        return dict(head=dict(name=self._get_head_name(), value=self._get_head_value()),
                    data=self._get_data_list(start=start, end=end),
                    info=dict(length=len(self.pivot_df)))

    def get_pivot_data_as_raw_data_result(self, start=0, end=None):
        self.pivot_df = self.pivot_df.T.reset_index()
        return self.get_pivot_data_result(start=start, end=end)

    def get_raw_data_result(self, index_list, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(self.df))))
        self.pivot_df = self.df.reset_index().iloc[index_range, :].loc[:, index_list]
        result = self.get_pivot_data_result()
        result.update(dict(info=dict(length=len(self.df))))
        return result

    def get_field_unique_value_list(self, column_name, dtype=None):
        #  面对极限的筛选条件可能出现对应列不存在的情况？ column_name 会莫名丢失？
        if column_name not in self.df.columns.tolist():
            log.debug("column: {column_name} not in {column_name_list}!".format(column_name=column_name, column_name_list=self.df.columns.tolist()))
            return []
        if dtype == field_consts.DTYPE_DATETIME_Y:
            return self.df[column_name].apply(self._change_dtype_datetime_y).unique().tolist()
        elif dtype == field_consts.DTYPE_DATETIME_Q:
            return self.df[column_name].apply(self._change_dtype_datetime_q).unique().tolist()
        elif dtype == field_consts.DTYPE_DATETIME_M:
            return self.df[column_name].apply(self._change_dtype_datetime_m).unique().tolist()
        elif dtype == field_consts.DTYPE_DATETIME_W:
            return self.df[column_name].apply(self._change_dtype_datetime_w).unique().tolist()
        elif dtype == field_consts.DTYPE_DATETIME_WD:
            return self.df[column_name].apply(self._change_dtype_datetime_wd).unique().tolist()
        elif dtype == field_consts.DTYPE_DATETIME_D:
            return self.df[column_name].apply(self._change_dtype_datetime_d).unique().tolist()
        else:
            return self.df[column_name].unique().tolist()

    def _change_dategroup_year(self, x):
        try:
            return "{:04d}年".format(x.year)
        except:
            return np.nan

    def _change_dategroup_quarter(self, x):
        try:
            return "{:04d}年第{:d}季度".format(x.year, x.quarter)
        except:
            return np.nan

    def _change_dategroup_month(self, x):
        try:
            return "{:04d}年{:02d}月".format(x.year, x.month)
        except:
            return np.nan

    def _change_dategroup_week(self, x):
        try:
            return "{:04d}年第{:02d}周".format(x.year, x.week)
        except:
            return np.nan

    def _change_dategroup_day(self, x):
        try:
            return "{:04d}年{:02d}月{:02d}日".format(x.year, x.month, x.day)
        except:
            return np.nan

    def _change_dtype_datetime_y(self, x):
        try:
            return "{:04d}年".format(x.year)
        except:
            return np.nan

    def _change_dtype_datetime_q(self, x):
        try:
            return "第{:d}季度".format(x.quarter)
        except:
            return np.nan

    def _change_dtype_datetime_m(self, x):
        try:
            return "{:02d}月".format(x.month)
        except:
            return np.nan

    def _change_dtype_datetime_w(selfself, x):
        try:
            return "第{:02d}周".format(x.week)
        except:
            return np.nan

    def _change_dtype_datetime_wd(self, x):
        try:
            return date_range.get_weekday(x.dayofweek)
        except:
            return np.nan

    def _change_dtype_datetime_d(self, x):
        try:
            return "{:02d}日".format(x.day)
        except:
            return np.nan

    def _change_aid_dategroup_year(self, x):
        try:
            return "{:04d}年".format(x.year + 1)
        except:
            return np.nan

    def _change_aid_dategroup_quarter(self, x):
        try:
            if x.quarter == 4:
                return "{:04d}年第{:d}季度".format(x.year + 1, 1)
            return "{:04d}年第{:d}季度".format(x.year, x.quarter + 1)
        except:
            return np.nan

    def _change_aid_dategroup_month(self, x):
        try:
            if x.month == 12:
                return "{:04d}年{:02d}月".format(x.year + 1, 1)
            return "{:04d}年{:02d}月".format(x.year, x.month + 1)
        except:
            return np.nan

    def _change_aid_dategroup_week(self, x):
        try:
            return "{:04d}年第{:02d}周".format(x.year, x.week)
        except:
            return np.nan

    def _change_aid_dategroup_day(self, x):
        try:
            return "{:04d}年{:02d}月{:02d}日".format(x.year, x.month, x.day)
        except:
            return np.nan

    def _change_aid_dtype_datetime_y(self, x):
        try:
            return "{:04d}年".format(x.year + 1)
        except:
            return np.nan

    def _change_aid_dtype_datetime_q(self, x):
        try:
            if x.quarter == 4:
                "第{:d}季度".format(1)
            return "第{:d}季度".format(x.quarter + 1)
        except:
            return np.nan

    def _change_aid_dtype_datetime_m(self, x):
        try:
            if x.month == 12:
                "{:02d}月".format(1)
            return "{:02d}月".format(x.month + 1)
        except:
            return np.nan

    def _change_aid_dtype_datetime_w(selfself, x):
        try:
            return "第{:02d}周".format(x.week)
        except:
            return np.nan

    def _change_aid_dtype_datetime_wd(self, x):
        try:
            return date_range.get_weekday(x.dayofweek)
        except:
            return np.nan

    def _change_aid_dtype_datetime_d(self, x):
        try:
            return "{:02d}日".format(x.day)
        except:
            return np.nan
