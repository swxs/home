# -*- coding: utf-8 -*-
# @Author  : SWXS
# @File    : DHelper_factory.py
# @Time    : 2018/2/28 15:04

from api.consts.bi import worktable as worktable_consts
from common.DHelper.DHelper_pandas import DHelper_pandas
from common.Exceptions import CommonException

def get_dhelper(worktable, create=False):
    if worktable.ttype in [worktable_consts.TABLE_TYPE_PIVOT, worktable_consts.TABLE_TYPE_CROSS]:
        if create:
            return DHelper_pandas(worktable.get_dataframe(), project_id=worktable.project_id)
        else:
            return DHelper_pandas()

    elif worktable.ttype in [worktable_consts.TABLE_TYPE_DASK]:
        try:
            from common.DHelper.DHelper_dask import DHelper_dask

            if create:
                return DHelper_dask(worktable.get_dataframe(), project_id=worktable.project_id)
            else:
                return DHelper_dask()
        except:
            raise CommonException("未安装指定组件!")

    elif worktable.ttype in [worktable_consts.TABLE_TYPE_MONGODB]:
        try:
            from common.DHelper.DHelper_mongo import DHelper_mongo
            if create:
                return DHelper_mongo(worktable.get_survey_id(), project_id=worktable.project_id)
            else:
                return DHelper_mongo()
        except:
            raise CommonException("未安装指定组件!")

    elif worktable.ttype in [worktable_consts.TABLE_TYPE_ODBC_PIVOT]:
        try:
            from common.DHelper.DHelper_ODBC import DHelper_ODBC
            if create:
                return DHelper_ODBC(worktable.get_table_name(), project_id=worktable.project_id)
            else:
                return DHelper_ODBC()
        except:
            raise CommonException("未安装指定组件!")
