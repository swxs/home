# -*- coding: utf-8 -*-
# @File    : DHelper_mongo.py
# @AUTH    : swxs
# @Time    : 2018/7/16 10:02

import string
import datetime
from collections import defaultdict

import pymongo
import numpy as np
import pandas as pd
import settings

from apps.bi import model_enums as field_enum
from commons.Echarts import option_consts as consts
from commons.DHelper.DHelper_base import DHelper_base
from motorengine.stages import (
    RawMatchStage,
    AddFieldsStage,
    GroupStage,
    RawProjectStage,
)


class DHelper_mongo(DHelper_base):
    def __init__(self, **kwargs):
        if kwargs.get("collection") is not None:
            super(DHelper_mongo, self).__init__()
            self.collection = kwargs.get("collection")

            self.new_column_dict = dict()
            self.match_stage_list = []
            self.changefields_stage_list = []

    def _do_filter(self):
        for filter in self._filter_list:
            if filter.dtype == field_enum.FIELD_DTYPE_DATETIME:
                ttype, start_time, end_time = filter.value_list
                filter_dict = {}
                if start_time:
                    filter_dict.update({"$gte": start_time})
                if end_time:
                    filter_dict.update({"$lt": end_time})
                self.match_stage_list.append(RawMatchStage(**{filter.column: filter_dict}))
            elif filter.dtype == field_enum.FIELD_DTYPE_DATETIME_Y:
                self.match_stage_list.append(RawMatchStage(**{filter.column: {"$in": [int(value) for value in filter.value_list]}}))
            elif filter.dtype == field_enum.FIELD_DTYPE_DATETIME_Q:
                self.match_stage_list.append(RawMatchStage(**{filter.column: {"$in": [int(value) for value in filter.value_list]}}))
            elif filter.dtype == field_enum.FIELD_DTYPE_DATETIME_M:
                self.match_stage_list.append(RawMatchStage(**{filter.column: {"$in": [int(value) for value in filter.value_list]}}))
            elif filter.dtype == field_enum.FIELD_DTYPE_DATETIME_W:
                self.match_stage_list.append(RawMatchStage(**{filter.column: {"$in": [int(value) for value in filter.value_list]}}))
            elif filter.dtype == field_enum.FIELD_DTYPE_DATETIME_WD:
                self.match_stage_list.append(RawMatchStage(**{filter.column: {"$in": [int(value) for value in filter.value_list]}}))
            elif filter.dtype == field_enum.FIELD_DTYPE_DATETIME_D:
                self.match_stage_list.append(RawMatchStage(**{filter.column: {"$in": [int(value) for value in filter.value_list]}}))
            else:
                self.match_stage_list.append(RawMatchStage(**{filter.column: {"$in": [int(value) for value in filter.value_list]}}))

    def _do_add_new_column(self):
        # self.new_column_dict = {column.new_column: column for column in self._new_column_list}
        for new_column in self._new_column_list:
            if new_column.dtype == field_enum.FIELD_DTYPE_DATETIME:
                if new_column.date_type == field_enum.FIELD_DATE_TYPE_YEAR:
                    self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                        '$dateToString': {
                            'format': "%Y",
                            'date': f"${new_column.column}"
                        }
                    }}))
                    self.new_column_dict.update({new_column.new_column: new_column})
                elif new_column.date_type == field_enum.FIELD_DATE_TYPE_QUARTER:
                    raise NotImplementedError()
                elif new_column.date_type == field_enum.FIELD_DATE_TYPE_MONTH:
                    self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                        '$dateToString': {
                            'format': "%Y-%m",
                            'date': f"${new_column.column}"
                        }
                    }}))
                    self.new_column_dict.update({new_column.new_column: new_column})
                elif new_column.date_type == field_enum.FIELD_DATE_TYPE_WEEK:
                    self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                        '$dateToString': {
                            'format': "%Y/%U",
                            'date': f"${new_column.column}"
                        }
                    }}))
                    self.new_column_dict.update({new_column.new_column: new_column})
                elif new_column.date_type == field_enum.FIELD_DATE_TYPE_DAY:
                    self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                        '$dateToString': {
                            'format': "%Y-%m-%d",
                            'date': f"${new_column.column}"
                        }
                    }}))
                    self.new_column_dict.update({new_column.new_column: new_column})
            elif new_column.dtype == field_enum.FIELD_DTYPE_DATETIME_Y:
                self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                    '$dateToString': {
                        'format': "%Y",
                        'date': f"${new_column.column}"
                    }
                }}))
                self.new_column_dict.update({new_column.new_column: new_column})
            elif new_column.dtype == field_enum.FIELD_DTYPE_DATETIME_Q:
                raise NotImplementedError()
            elif new_column.dtype == field_enum.FIELD_DTYPE_DATETIME_M:
                self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                    '$dateToString': {
                        'format': "%m",
                        'date': f"${new_column.column}"
                    }
                }}))
                self.new_column_dict.update({new_column.new_column: new_column})
            elif new_column.dtype == field_enum.FIELD_DTYPE_DATETIME_W:
                self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                    '$dateToString': {
                        'format': "%U",
                        'date': f"${new_column.column}"
                    }
                }}))
                self.new_column_dict.update({new_column.new_column: new_column})
            elif new_column.dtype == field_enum.FIELD_DTYPE_DATETIME_WD:
                self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                    '$dateToString': {
                        'format': "%w",
                        'date': f"${new_column.column}"
                    }
                }}))
                self.new_column_dict.update({new_column.new_column: new_column})
            elif new_column.dtype == field_enum.FIELD_DTYPE_DATETIME_D:
                self.changefields_stage_list.append(AddFieldsStage(**{f"{new_column.column}": {
                    '$dateToString': {
                        'format': "%d",
                        'date': f"${new_column.column}"
                    }
                }}))
                self.new_column_dict.update({new_column.new_column: new_column})
            else:
                self.new_column_dict.update({new_column.new_column: new_column})

    def _do_drilldown(self):
        for drilldown in self._drilldown_list:
            self.drilldown.update({drilldown.new_column: drilldown.value})

    def do_preprocess(self):
        self._do_filter()
        self._do_add_new_column()
        # self._do_drilldown()

    def get_aggfunc(self, pivot):
        if pivot.func == field_enum.FIELD_AGG_TYPE_MEAN:
            return {pivot.new_column: {"$avg": pivot.new_column}}
        elif pivot.func == field_enum.FIELD_AGG_TYPE_COUNT:
            return {pivot.new_column: {"$sum": 1}}
        return {}

    async def _get_serie_data(self, pivot_list):
        if not pivot_list:
            return pd.DataFrame()
        index_list = []
        groups = {}
        projects = {"_id": 0}
        index_column_list = []
        value_column_list = []
        for pivot in pivot_list:
            if not index_list:
                for index in pivot.index_list:
                    index_list.append(index)
                    projects[index] = f"$_id.{index}"
                    index_column_list.append(index)

            value_column_list.append(pivot.new_column)
            if pivot.func == field_enum.FIELD_AGG_TYPE_MEAN:
                groups[pivot.new_column] = {"$avg": f"${self.new_column_dict.get(pivot.new_column).column}"}
                projects[pivot.new_column] = 1
            elif pivot.func == field_enum.FIELD_AGG_TYPE_COUNT:
                groups[pivot.new_column] = {"$sum": 1}
                projects[pivot.new_column] = 1
            elif pivot.func == field_enum.FIELD_AGG_TYPE_SUM:
                groups[pivot.new_column] = {"$sum": f"${self.new_column_dict.get(pivot.new_column).column}"}
                projects[pivot.new_column] = 1
            elif pivot.func == field_enum.FIELD_AGG_TYPE_NUNIQ:
                groups[pivot.new_column] = {"addToSet": f"${self.new_column_dict.get(pivot.new_column).column}"}
                projects[pivot.new_column] = {"$size": f"${pivot.new_column}"}
            else:
                pass

        pipelines = []
        pipelines.extend(self.match_stage_list)
        pipelines.extend(self.changefields_stage_list)
        if index_list[0] == consts.ALL:
            pipelines.append(AddFieldsStage(
                **{consts.ALL: consts.ALL}
            ))
            pipelines.append(GroupStage(
                {consts.ALL: consts.ALL},
                **groups
            ))
        else:
            pipelines.append(GroupStage(
                {index: f"${self.new_column_dict.get(index).column}" for index in index_list},
                **groups
            ))
        pipelines.append(RawProjectStage(
            **projects
        ))
        for p in pipelines:
            print(p.to_query())
        cursor = await self.collection.aggregate(pipelines)
        self.result = await cursor.to_list(1000)
        self.tmp_df = pd.DataFrame(pd.Series(x.__dict__) for x in self.result)
        return self.tmp_df.set_index(index_column_list)[value_column_list].T

    async def _get_main_df(self, pivot_list, has_colortag, fillna=settings.NONE_DATA):
        tmp_df = await self._get_serie_data(pivot_list)

        def get_column_name(column):
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
                new_columns_names = tmp_df.columns.names[:-1]
                new_columns = list()
                for column in tmp_df.columns.droplevel(level=-1).tolist():
                    if column not in new_columns:
                        new_columns.append(column)
                data_dict = dict()
                for i, data in enumerate(all_data):
                    colortag_name = get_column_name(tmp_df.columns[i][-1])
                    if colortag_name not in data_dict:
                        data_dict[colortag_name] = dict()
                    data_dict[colortag_name][get_column_name(tmp_df.columns[i][0:-1])] = data
                # colortag_columns = tmp_df.columns.levels[-1].tolist()
                # for columns in colortag_columns:
                #     data_dict[get_column_name(columns)] = list()
                # old_type = None
                # for i, data in enumerate(all_data):
                #     if old_type != tmp_df.columns[i][-2]:
                #         for columns in colortag_columns:
                #             data_dict[get_column_name(columns)].append(np.nan)
                #         old_type = tmp_df.columns[i][-2]
                #     data_dict[get_column_name(tmp_df.columns[i][-1])].pop()
                #     data_dict[get_column_name(tmp_df.columns[i][-1])].append(data)
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
        return tmp_df

    async def _get_sub_df(self, pivot_list, has_colortag, fillna=settings.NONE_DATA):
        df = await self._get_serie_data(pivot_list)
        return df

    async def do_pivot(self, has_color_tag, fillna="-", change_func=None):
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

    def do_rank(self, dtype, ascending, sortIndex, xAxisCount=None):
        pass

    def do_refresh(self, field_id_list):
        pass

    def _get_head_name(self, df=None):
        if df.columns.name:
            return [df.columns.name]
        else:
            return list(df.columns.names)

    def _get_head_value(self, df=None):
        return df.columns.tolist()

    def _get_data_list(self, df=None, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(df))))
        return [dict(name=str(field_name), value=df.loc[field_name].tolist())
                for field_name in df.iloc[index_range].index.tolist()]

    def get_pivot_data(self, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(self.pivot_df))))
        return self.pivot_df.iloc[index_range, :]

    def get_pivot_data_result(self, start=0, end=None):
        return dict(
            head=dict(name=self._get_head_name(df=self.pivot_df), value=self._get_head_value(df=self.pivot_df)),
            data=self._get_data_list(df=self.pivot_df, start=start, end=end),
            info=dict(length=len(self.pivot_df))
        )

    def get_pivot_group_data_result(self, color_tag=False, start=0, end=None):
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
        self.pivot_df = self.pivot_df.T.reset_index()
        return self.get_pivot_data_result(start=start, end=end)

    def get_pivot_group_data_as_raw_data_result(self, color_tag=False, start=0, end=None):
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

    def get_field_unique_value_list(self, column, dtype):
        return self.collection.distinct(column.col)

    async def get_base_data(self, start=0, end=None):
        cursor = await self.collection.find()
        self.result = await cursor.to_list(end)
        return pd.DataFrame(pd.Series(x.__dict__) for x in self.result)
