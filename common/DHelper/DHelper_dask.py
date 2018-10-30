# -*- coding: utf-8 -*-
# @Author  : SWXS
# @File    : DHelper_dask.py
# @Time    : 2018/3/6 11:27

import datetime
import string
import numpy as np
import pandas as pd
import dask.dataframe as dd
from distributed import Client

from common.decorator_utils import timeit
from common.date_range import get_weekday
from api.bi.field import enum as field_enum
from common.df_exception import NoDataException
from common.DHelper.DHelper_pandas import DHelper_pandas


class DHelper_dask(DHelper_pandas):
    def __new__(cls, *args):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.__singleton__ = singleton = object.__new__(cls)
        return singleton
    
    def __init__(self, df=None, project_id=None):
        if not hasattr(self, "__client__"):
            self.__client__ = Client('127.0.0.1:8786')
        super(DHelper_dask, self).__init__(df)
    
    def init_df(self, df):
        self.df = self.__client__.persist(dd.from_pandas(df, npartitions=4))
    
    def _get_series(self, grouped_dataframe, column_name, index_list, func):
        if (callable(func)):
            agg_series = grouped_dataframe.agg({column_name: func})[column_name].compute()
        else:
            def test_func(df):
                if len(df) > 0:
                    df[column_name] = eval(func)
                return df
            
            df = grouped_dataframe.apply(test_func).compute()
            if len(df) == 0:
                agg_series = pd.Series()
            else:
                agg_series = df.groupby(index_list).agg({column_name: np.mean})[column_name]
        return agg_series
    
    def do_refresh(self, field_id_list):
        pass
    
    def get_base_data(self, start=0, end=None):
        index_range = slice(*(slice(start, end).indices(len(self.df))))
        return self.df.compute().iloc[index_range, :]
    
    def get_field_unique_value_list(self, column_name, dtype=None):
        if dtype == field_enum.DTYPE_DATETIME_Y:
            return self.df.compute()[column_name].apply(self._change_dtype_datetime_y).unique().tolist()
        elif dtype == field_enum.DTYPE_DATETIME_Q:
            return self.df.compute()[column_name].apply(self._change_dtype_datetime_q).unique().tolist()
        elif dtype == field_enum.DTYPE_DATETIME_M:
            return self.df.compute()[column_name].apply(self._change_dtype_datetime_m).unique().tolist()
        elif dtype == field_enum.DTYPE_DATETIME_W:
            return self.df.compute()[column_name].apply(self._change_dtype_datetime_w).unique().tolist()
        elif dtype == field_enum.DTYPE_DATETIME_WD:
            return self.df.compute()[column_name].apply(self._change_dtype_datetime_wd).unique().tolist()
        elif dtype == field_enum.DTYPE_DATETIME_D:
            return self.df.compute()[column_name].apply(self._change_dtype_datetime_d).unique().tolist()
        else:
            return self.df.compute()[column_name].unique().tolist()
