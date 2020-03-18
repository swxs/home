# -*- coding: utf-8 -*-
# @File    : MemorizeFileTmp.py
# @AUTH    : swxs
# @Time    : 2019/7/26 18:06

import os
import tables
import settings
from functools import wraps
from commons import log_utils
from commons import df_utils

log = log_utils.get_logging("MemorizeFileTmp.py")

OBJ_DICT = {}


def remove_all_data_memorize():
    """
    简介
    ----------
    清除当前系统内所有工作表数据缓存
    
    """
    for key in OBJ_DICT:
        remove_key(key)


def remove_data_memorize_by_worktable_id(worktable_id):
    """
    简介
    ----------
    清除当前系统内所有指定工作表的所有数据缓存
    
    参数
    ----------
    worktable_id : 
        工作表id
    """
    delete_keys_list = list()
    for key in OBJ_DICT:
        if str(key.split("_")[-1]) == str(worktable_id):
            delete_keys_list.append(key)
    for key in delete_keys_list:
        remove_key(key)


def remove_key(key):
    """
    简介
    ----------
    清除当前系统内所有签名的所有数据缓存
    
    参数
    ----------
    key : 
        签名
    """
    if key in OBJ_DICT:
        signature, filename = OBJ_DICT[key]
        filepath = _get_filepath(filename)
        try:
            # 这个文件存在未被关闭的句柄, 尝试关闭
            count = df_utils.close_hdf_handlers(filepath)
            os.remove(filepath)
        except Exception as e:
            # 其他未知问题
            log.exception(f"文件[{key}]无法被删除！")
            pass
        del OBJ_DICT[key]


def _get_filepath(filename):
    """
    简介
    ----------
    获取文件地址
    
    参数
    ----------
    filename : 
        文件名
    
    返回
    -------
    path
    """
    return os.path.join(settings.TMPFS_PATH, f"{filename}.h5")


def memorize_file(function):
    """
    简介
    ----------
    缓存工作表数据源
    通过 CACHE_WORKTABLE_MODE 配置是否开启缓存
    
    参数
    ----------
    function : 
    
        返回
        ------- 
        pd.Dataframe()
    
    返回
    -------
    wrapper
    """
    from apps.bi import worktable_utils
    @wraps(function)
    async def helper(*args):
        if not settings.CACHE_WORKTABLE_MODE:
            return await function(*args)
        worktable = args[0].worktable
        key = "{0}_{1}".format(function.__name__, worktable.id)
        if key in OBJ_DICT:
            signature, filename = OBJ_DICT[key]
            current_signature = await worktable_utils.get_signature(worktable)
            if signature != current_signature:
                log.warning(f"{key} has changed!")
                # 清理老数据
                remove_key(key)
                ret_obj = await function(*args)
                try:
                    OBJ_DICT[key] = (current_signature, current_signature)
                    filepath = _get_filepath(current_signature)
                    df_utils.save_dataframe_by_file(filepath, ret_obj, format="table")
                except TypeError as e:
                    log.warning(f"文件[{filepath}]数据源[{worktable.oid}]存在混合类型数据，部分字段存在异常")
                    for index, dtype in ret_obj.dtypes.iteritems():
                        if dtype == "object":
                            ret_obj[index] = ret_obj[index].map(str).map(str.strip)
                    try:
                        df_utils.save_dataframe_by_file(filepath, ret_obj, format="table")
                    except Exception as e:
                        log.exception(f"文件[{filepath}]写入失败！")
                        remove_key(key)
                except Exception as e:
                    log.exception(f"文件[{filepath}]写入失败！")
                    remove_key(key)
            else:
                try:
                    filepath = _get_filepath(filename)
                    if os.path.isfile(filepath):
                        ret_obj = df_utils.get_dataframe_by_file(filepath)
                        # 这里的问题是文件会莫名损坏
                        # tables.exceptions.NoSuchNodeError: group ``/table`` does not have a child named ``block0_items``
                        if ret_obj.empty:
                            ret_obj = await function(*args)
                            df_utils.save_dataframe_by_file(filepath, ret_obj, format="table")
                    else:
                        ret_obj = await function(*args)
                        df_utils.save_dataframe_by_file(filepath, ret_obj, format="table")
                except Exception as e:
                    log.exception(f"{key}'s file has broken!")
                    remove_key(key)
                    ret_obj = await function(*args)
                    try:
                        OBJ_DICT[key] = (current_signature, current_signature)
                        df_utils.save_dataframe_by_file(filepath, ret_obj, format="table")
                    except TypeError as e:
                        log.warning(f"文件[{filepath}]数据源[{worktable.oid}]存在混合类型数据，部分字段存在异常")
                        for index, dtype in ret_obj.dtypes.iteritems():
                            if dtype == "object":
                                ret_obj[index] = ret_obj[index].map(str).map(str.strip)
                        try:
                            df_utils.save_dataframe_by_file(filepath, ret_obj, format="table")
                        except Exception as e:
                            log.exception(f"文件[{filepath}]写入失败！")
                            remove_key(key)
                    except ValueError:
                        # 这里的写入会报文件已打开的问题
                        # ValueError:
                        # The file '/mnt/tmp_bi/0363664992114017931f95deaabed0e1.h5' is already opened.
                        # Please close it before reopening in write mode.
                        remove_key(key)
        else:
            current_signature = await worktable_utils.get_signature(worktable)
            ret_obj = await function(*args)
            try:
                OBJ_DICT[key] = (current_signature, current_signature)
                filepath = _get_filepath(current_signature)
                df_utils.save_dataframe_by_file(filepath, ret_obj, format="table")
            except tables.exceptions.HDF5ExtError:
                # 目前不清楚怎么处理
                # tables.exceptions.HDF5ExtError:
                # HDF5 error back trace File "H5F.c", line 445,
                # in H5Fcreate unable to create file File "H5Fint.c", line 1519,
                # in H5F_open unable to lock the file File "H5FD.c", line 1650,
                # in H5FD_lock driver lock request failed File "H5FDsec2.c", line 941,
                # in H5FD_sec2_lock unable to lock file, errno = 11,
                # error message = 'Resource temporarily unavailable'
                # End of HDF5 error back trace Unable to open/create file
                # '/mnt/tmp_bi/1eb245256ceee9dda0cf67a39a2b01e6.h5'
                remove_key(key)
            except TypeError as e:
                log.warning(f"文件[{filepath}]数据源[{worktable.oid}]存在混合类型数据，部分字段存在异常")
                for index, dtype in ret_obj.dtypes.iteritems():
                    if dtype == "object":
                        ret_obj[index] = ret_obj[index].map(str).map(str.strip)
                try:
                    df_utils.save_dataframe_by_file(filepath, ret_obj, format="table")
                except Exception as e:
                    log.exception(f"文件[{filepath}]写入失败！")
                    remove_key(key)
            except Exception as e:
                log.exception(f"文件[{filepath}]写入失败！")
                remove_key(key)
        log.info(OBJ_DICT)
        return ret_obj

    return helper
