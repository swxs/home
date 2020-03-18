# -*- coding: utf-8 -*-
# @File    : DataHelper_pandas.py
# @AUTH    : swxs
# @Time    : 2019/4/22 14:32

import numpy as np
import pandas as pd
from commons.Helpers import Helper_daterange as date_range

class DataHelper_pandas():
    @staticmethod
    def _change_dategroup_year(x):
        try:
            return "{:04d}年".format(x.year)
        except Exception:
            return np.nan

    @staticmethod
    def _change_dategroup_quarter(x):
        try:
            return "{:04d}年第{:d}季度".format(x.year, x.quarter)
        except:
            return np.nan

    @staticmethod
    def _change_dategroup_month(x):
        try:
            return "{:04d}年{:02d}月".format(x.year, x.month)
        except:
            return np.nan

    @staticmethod
    def _change_dategroup_week(x):
        try:
            return "{:04d}年第{:02d}周".format(x.year, x.week)
        except:
            return np.nan

    @staticmethod
    def _change_dategroup_day(x):
        try:
            return "{:04d}年{:02d}月{:02d}日".format(x.year, x.month, x.day)
        except:
            return np.nan

    @staticmethod
    def _change_dtype_datetime_y(x):
        try:
            return "{:04d}年".format(x.year)
        except:
            return np.nan

    @staticmethod
    def _change_dtype_datetime_q(x):
        try:
            return "第{:d}季度".format(x.quarter)
        except:
            return np.nan

    @staticmethod
    def _change_dtype_datetime_m(x):
        try:
            return "{:02d}月".format(x.month)
        except:
            return np.nan

    @staticmethod
    def _change_dtype_datetime_w(x):
        try:
            return "第{:02d}周".format(x.week)
        except:
            return np.nan

    @staticmethod
    def _change_dtype_datetime_wd(x):
        try:
            return date_range.get_weekday(x.dayofweek)
        except:
            return np.nan

    @staticmethod
    def _change_dtype_datetime_d(x):
        try:
            return "{:02d}日".format(x.day)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dategroup_year(x):
        try:
            return "{:04d}年".format(x.year + 1)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dategroup_quarter(x):
        try:
            if x.quarter == 4:
                return "{:04d}年第{:d}季度".format(x.year + 1, 1)
            return "{:04d}年第{:d}季度".format(x.year, x.quarter + 1)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dategroup_month(x):
        try:
            if x.month == 12:
                return "{:04d}年{:02d}月".format(x.year + 1, 1)
            return "{:04d}年{:02d}月".format(x.year, x.month + 1)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dategroup_week(x):
        try:
            tmp_x = x + pd.Timedelta(1, unit='W')
            return "{:04d}年第{:02d}周".format(tmp_x.year, tmp_x.week)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dategroup_day(x):
        try:
            tmp_x = x + pd.Timedelta(1, unit='D')
            return "{:04d}年{:02d}月{:02d}日".format(tmp_x.year, tmp_x.month, tmp_x.day)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dtype_datetime_y(x):
        try:
            return "{:04d}年".format(x.year + 1)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dtype_datetime_q(x):
        try:
            if x.quarter == 4:
                "第{:d}季度".format(1)
            return "第{:d}季度".format(x.quarter + 1)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dtype_datetime_m(x):
        try:
            if x.month == 12:
                "{:02d}月".format(1)
            return "{:02d}月".format(x.month + 1)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dtype_datetime_w(x):
        try:
            tmp_x = x + pd.Timedelta(1, unit='W')
            return "第{:02d}周".format(tmp_x.week)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dtype_datetime_wd(x):
        try:
            return date_range.get_weekday(x.dayofweek)
        except:
            return np.nan

    @staticmethod
    def _change_aid_dtype_datetime_d(x):
        try:
            tmp_x = x + pd.Timedelta(1, unit='D')
            return "{:02d}日".format(tmp_x.day)
        except:
            return np.nan

    @classmethod
    def add_date_column(cls, df, column_name):
        df[f"{column_name}_y"] = df[column_name].agg(cls._change_dtype_datetime_y)
        df[f"{column_name}_q"] = df[column_name].agg(cls._change_dtype_datetime_q)
        df[f"{column_name}_m"] = df[column_name].agg(cls._change_dtype_datetime_m)
        df[f"{column_name}_w"] = df[column_name].agg(cls._change_dtype_datetime_w)
        df[f"{column_name}_wd"] = df[column_name].agg(cls._change_dtype_datetime_wd)
        df[f"{column_name}_d"] = df[column_name].agg(cls._change_dtype_datetime_d)
        df[f"{column_name}_year"] = df[column_name].agg(cls._change_dategroup_year)
        df[f"{column_name}_quarter"] = df[column_name].agg(cls._change_dategroup_quarter)
        df[f"{column_name}_month"] = df[column_name].agg(cls._change_dategroup_month)
        df[f"{column_name}_week"] = df[column_name].agg(cls._change_dategroup_week)
        df[f"{column_name}_day"] = df[column_name].agg(cls._change_dategroup_day)

        df[f"{column_name}_aid_y"] = df[column_name].agg(cls._change_aid_dtype_datetime_y)
        df[f"{column_name}_aid_q"] = df[column_name].agg(cls._change_aid_dtype_datetime_q)
        df[f"{column_name}_aid_m"] = df[column_name].agg(cls._change_aid_dtype_datetime_m)
        df[f"{column_name}_aid_w"] = df[column_name].agg(cls._change_aid_dtype_datetime_w)
        df[f"{column_name}_aid_wd"] = df[column_name].agg(cls._change_aid_dtype_datetime_wd)
        df[f"{column_name}_aid_d"] = df[column_name].agg(cls._change_aid_dtype_datetime_d)
        df[f"{column_name}_aid_year"] = df[column_name].agg(cls._change_aid_dategroup_year)
        df[f"{column_name}_aid_quarter"] = df[column_name].agg(cls._change_aid_dategroup_quarter)
        df[f"{column_name}_aid_month"] = df[column_name].agg(cls._change_aid_dategroup_month)
        df[f"{column_name}_aid_week"] = df[column_name].agg(cls._change_aid_dategroup_week)
        df[f"{column_name}_aid_day"] = df[column_name].agg(cls._change_aid_dategroup_day)
