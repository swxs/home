# -*- coding: utf-8 -*-
# @File    : df_utils.py
# @AUTH    : swxs
# @Time    : 2018/8/30 9:57

import os
import glob
import math
import datetime
import pandas as pd
import numpy as np
import tables
import collections
import settings
from common.Helpers import Helper_daterange as date_range

try:
    Period = pd.Period
except AttributeError:
    Period = pd._period.Period


from commons import log_utils

logger = log_utils.get_logging(name='df_utils', file_name='df_utils.log')


def data_filter_type_changer(obj):
    if isinstance(obj, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
        return str(int(obj))
    elif isinstance(obj, (np.float, np.float16, np.float32, np.float64)):
        if math.isnan(obj):
            return
        elif np.isinf(obj):
            return
        else:
            return float(obj)

    else:
        return obj


def encode_data(obj):
    if isinstance(obj, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
        return str(int(obj))
    elif isinstance(obj, (np.float, np.float16, np.float32, np.float64)):
        if math.isnan(obj):
            return "N/A"
        elif np.isinf(obj):
            return "Inf"
        else:
            return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.datetime64):
        try:
            return pd.to_datetime(str(obj)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            return "N/A"
    elif isinstance(obj, (datetime.datetime, Period)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return obj


def _get_hdf_keys(fname):
    try:
        with pd.HDFStore(fname, mode="r+") as hdf:
            key_list = hdf.keys()
    except Exception:
        key_list = []
    return key_list


def copy_dataframe_by_filename(src_filename, dst_filename):
    ext = os.path.splitext(src_filename)[1].lower()
    if ext in ['.h5']:
        key_list = _get_hdf_keys(src_filename)
        for key in key_list:
            df = get_dataframe_by_file(src_filename, key=key)
            save_dataframe_by_file(dst_filename, df, key=key, format="table")
    else:
        df = get_dataframe_by_file(src_filename)
        save_dataframe_by_file(dst_filename, df)


def save_dataframe_by_file(abs_filename, df, key="table", **kwargs):
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
        df.to_hdf(abs_filename, key, **kwargs)
    else:
        raise Exception('not supported yet')


def get_dataframe_by_file(abs_filename, key="table", **kwargs):
    ext = os.path.splitext(abs_filename)[1].lower()

    if ext == '.csv':
        try:
            df = pd.read_csv(abs_filename, encoding='utf8', **kwargs)
        except UnicodeDecodeError:
            df = pd.read_csv(abs_filename, encoding='gb18030', **kwargs)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(abs_filename, **kwargs)
    elif ext in ['.h5']:
        try:
            kwargs["mode"] = kwargs.get("mode", "r")
            df = pd.read_hdf(abs_filename, key=key, **kwargs)
            if df.empty:
                logger.error(f"PID: {os.getpid()}, {abs_filename} key[{key}] has no data!")
        except KeyError:
            logger.error(f"PID: {os.getpid()}, {abs_filename} key[{key}] exception [KeyError]!")
            df = pd.DataFrame()
        except FileNotFoundError:
            logger.error(f"PID: {os.getpid()}, {abs_filename} key[{key}] exception [FileNotFoundError]!")
            df = pd.DataFrame()
    else:
        raise Exception('not supported yet')
    return df


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


def get_signature_by_name(filename):
    return f"{os.path.getctime(filename)}_{os.path.getmtime(filename)}_{os.path.getsize(filename)}"


def get_filepath(filepath, filename):
    if '..' in filename or '/' in filename or '\\' in filename:
        raise Exception('bad df filename')
    return os.path.join(filepath, filename)


def get_dataframe_with_keylist(abs_filename, key_list):
    df_list = [get_dataframe_by_file(abs_filename, key=x) for x in key_list]
    if df_list:
        return pd.concat(df_list, sort=False, ignore_index=True)
    else:
        return pd.DataFrame()


def get_dateframe_by_timestamp(abs_filename, timestamp_start=None, timestamp_end=None):
    all_key_list = _get_hdf_keys(abs_filename)
    key_list = list()
    for key in all_key_list:
        try:
            tmp_key = int(key.replace("/", "").replace("df_", ""))
            if (timestamp_start is not None) and (tmp_key <= timestamp_start):
                continue
            if (timestamp_end is not None) and (tmp_key >= timestamp_end):
                continue
            key_list.append(key)
        except Exception:
            pass
    if key_list:
        return get_dataframe_with_keylist(abs_filename, key_list)
    else:
        return pd.DataFrame()


def get_concat_dateframe_by_timestamp(abs_filename_list, timestamp_start=None, timestamp_end=None):
    df_list = [
        get_dateframe_by_timestamp(abs_filename, timestamp_start, timestamp_end) for abs_filename in abs_filename_list
    ]
    if df_list:
        return pd.concat(df_list, sort=False, ignore_index=True)
    else:
        return pd.DataFrame()


def get_column_col_list(filepath):
    newpath = os.path.join(settings.DATA_FILE_PATH, filepath)
    try:
        df1 = pd.read_csv(os.path.join(newpath, 'All_Data_Original.csv'), encoding='utf8', skiprows=0, nrows=None)
    except UnicodeDecodeError:
        df1 = pd.read_csv(os.path.join(newpath, 'All_Data_Original.csv'), encoding='gb18030', skiprows=0, nrows=None)
    try:
        df2 = pd.read_csv(os.path.join(newpath, 'All_Data_Readable.csv'), encoding='utf8', skiprows=0, nrows=None)
    except UnicodeDecodeError:
        df2 = pd.read_csv(os.path.join(newpath, 'All_Data_Readable.csv'), encoding='gb18030', skiprows=0, nrows=None)
    df2.drop('答题时长', axis=1, inplace=True)
    return df1.columns, df2.columns


def make_data_clean(data):
    max_length = 0
    length_dict = {}
    for k, v in data.items():
        length = len(v)
        length_dict[k] = length
        if length > max_length:
            max_length = length

    for k, v in data.items():
        for _ in range(max_length - length_dict[k]):
            data[k].append(np.nan)

    return data
