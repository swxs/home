# -*- coding: utf-8 -*-
# @File    : df_utils.py
# @AUTH    : swxs
# @Time    : 2018/8/30 9:57

import os
import logging
import tables
import pandas as pd

try:
    Period = pd.Period
except AttributeError:
    Period = pd._period.Period

from ..Helpers.Helper_rwlock import ReadLocked, WriteLocked


logger = logging.getLogger('helper.df_utils')


@ReadLocked(timeout=1000 * 60)
async def _get_hdf_keys(fname):
    key_list = []
    try:
        with pd.HDFStore(fname, mode="r") as hdf:
            key_list = hdf.keys()
    except Exception:
        pass
    return key_list


@WriteLocked(timeout=1000 * 60)
async def save_dataframe_by_file(abs_filename, df, key="table", **kwargs):
    ext = os.path.splitext(abs_filename)[1].lower()
    if ext == '.csv':
        kwargs["index"] = kwargs.get("index", False)
        kwargs["encoding"] = kwargs.get("encoding", 'gb18030')
        df.to_csv(abs_filename, **kwargs)
    elif ext in ['.xlsx', '.xls']:
        kwargs["index"] = kwargs.get("index", False)
        writer = pd.ExcelWriter(abs_filename)
        df.to_excel(writer, "Sheet1", **kwargs)
        writer.save()
        writer.close()
    elif ext in ['.h5']:
        kwargs["mode"] = kwargs.get("mode", "w")
        try:
            df.to_hdf(abs_filename, key, **kwargs)
        except ValueError as e:
            closed = close_hdf_handlers(abs_filename)
            if closed > 0:
                df.to_hdf(abs_filename, key, **kwargs)
            else:
                raise e
    elif ext in ['.parquet']:
        kwargs.pop('format', None)
        kwargs.pop('allow_truncated_timestamps', True)
        df.to_parquet(abs_filename, **kwargs)
    else:
        raise Exception('not supported yet')


@ReadLocked(timeout=1000 * 60)
async def get_dataframe_by_file(abs_filename, key="table", raise_ext=False, **kwargs):
    ext = os.path.splitext(abs_filename)[1].lower()
    if ext == '.csv':
        kwargs.pop('columns', None)
        try:
            df = pd.read_csv(abs_filename, encoding='utf8', **kwargs)
        except UnicodeDecodeError:
            df = pd.read_csv(abs_filename, encoding='gb18030', **kwargs)
    elif ext in ['.xlsx', '.xls']:
        kwargs.pop('columns', None)
        df = pd.read_excel(abs_filename, **kwargs)
    elif ext in ['.h5']:
        kwargs.pop('columns', None)
        if not key:
            logger.error(f"PID: {os.getpid()}, {abs_filename} key empty!")
            key = "table"
        try:
            kwargs["mode"] = kwargs.get("mode", "r")
            df = pd.read_hdf(abs_filename, key=key, **kwargs)
            if df.empty:
                logger.error(f"PID: {os.getpid()}, {abs_filename} key[{key}] has no data!")
        except KeyError as e:
            logger.exception(f"PID: {os.getpid()}, {abs_filename} key[{key}] exception [KeyError]!")
            if raise_ext:
                raise e
            df = pd.DataFrame()
        except FileNotFoundError as e:
            logger.exception(f"PID: {os.getpid()}, {abs_filename} key[{key}] exception [FileNotFoundError]!")
            if raise_ext:
                raise e
            df = pd.DataFrame()
        except Exception as e:
            logger.exception(f"PID: {os.getpid()}, {abs_filename} key[{key}] exception [Unknown]!")
            if raise_ext:
                raise e
            df = pd.DataFrame()
    elif ext in ['.parquet']:
        try:
            if not kwargs.get("columns"):
                kwargs.pop("columns", None)
            df = pd.read_parquet(abs_filename, **kwargs)
        except Exception as e:
            logger.exception(f"PID: {os.getpid()}, {abs_filename} key[{key}] exception [Unknown]!")
            if raise_ext:
                raise e
            df = pd.DataFrame()
    else:
        raise Exception('not supported yet')
    return df


async def append_dataframe_by_hdfs_file(abs_filename, df, key="table"):
    """
    简介
    ----------
    原子地追加数据

    参数
    ----------
    abs_filename :

    key :

    df :


    返回
    ----------

    """
    async with WriteLocked(abs_filename, timeout=1000 * 60 * 2):
        total_df = (await get_dataframe_by_file.__wrapped__(abs_filename, key=key)).append(df, sort=False)
        if (not total_df.empty) and len(total_df) > 0:
            await save_dataframe_by_file.__wrapped__(abs_filename, total_df, key=key, mode="a", format="table")
            return True
        else:
            return False


async def change_dataframe_by_hdf5_file(abs_filename, condition, changer, key="table"):
    """
    简介
    ----------
    原子地修改数据
    todo: 完善condition、changer的机制， 允许动态判断条件及指定替换逻辑

    参数
    ----------
    abs_filename :

    time :

    condition :

    changer :


    返回
    ----------

    """
    async with WriteLocked(abs_filename, timeout=1000 * 60 * 2):
        df = await get_dataframe_by_file.__wrapped__(abs_filename, key=key)
        if (not df.empty) and len(df.loc[condition]) > 0:
            df.loc[condition] = changer
            await save_dataframe_by_file.__wrapped__(abs_filename, df, key=key, mode="a", format="table")
            return True
        return False


async def delete_dataframe_by_hdf5_file(abs_filename, condition, key="table"):
    """
    简介
    ----------
    原子地删除数据
    todo: 完善condition的机制， 允许动态判断条件

    参数
    ----------
    abs_filename :

    time :

    condition :


    返回
    ----------

    """
    async with WriteLocked(abs_filename, timeout=1000 * 60 * 2):
        df = await get_dataframe_by_file.__wrapped__(abs_filename, key=key)
        if (not df.empty) and len(df.loc[condition]) > 0:
            df = df[~(condition)]
            await save_dataframe_by_file.__wrapped__(abs_filename, df, key=key, mode="a", format="table")
            return True
        return False


def close_hdf_handlers(filename):
    count = 0
    handlers = list(tables.file._open_files.handlers)
    for fileh in handlers:
        if fileh.filename == filename:
            fileh.close()
            count += 1
        else:
            logger.info(f"filename: [{filename}] & filehandler: [{fileh.filename}]")
    return count


async def get_dateframe_in_keylist(abs_filename, key_list):
    df_list = []
    async with ReadLocked(abs_filename, timeout=1000 * 60 * len(key_list)):
        for key in key_list:
            df_list.append(await get_dataframe_by_file.__wrapped__(abs_filename, key=key))
    if df_list:
        return pd.concat(df_list, sort=False, ignore_index=True)
    else:
        return pd.DataFrame()


async def get_dateframe_in_daterange(abs_filename, timestamp_start=None, timestamp_end=None):
    all_key_list = await _get_hdf_keys(abs_filename)
    key_list = list()
    for key in all_key_list:
        try:
            tmp_key = int(key.replace("/", "").replace("df_", ""))
            if (timestamp_start is not None) and (tmp_key <= timestamp_start):
                continue
            if (timestamp_end is not None) and (tmp_key > timestamp_end):
                continue
            key_list.append(key)
        except Exception:
            pass
    if key_list:
        return await get_dateframe_in_keylist(abs_filename, key_list)
    else:
        return pd.DataFrame()


async def get_dateframe_in_filelist_in_daterange(abs_filename_list, timestamp_start=None, timestamp_end=None):
    df_list = [
        await get_dateframe_in_daterange(abs_filename, timestamp_start, timestamp_end)
        for abs_filename in abs_filename_list
    ]
    if df_list:
        return pd.concat(df_list, sort=False, ignore_index=True)
    else:
        return pd.DataFrame()
