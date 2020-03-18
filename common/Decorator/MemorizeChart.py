# -*- coding: utf-8 -*-
# @File    : MemorizeChart.py
# @AUTH    : swxs
# @Time    : 2019/3/7 17:23

import hashlib
import functools
from tornado.util import ObjectDict
import settings
from exceptions import *
from apps.errors import AppResourceError
from commons.Helpers.Helper_MsgpackEncoder import (dumps, loads)
from commons.Helpers.Helper_JsonEncoder import dumps as json_dumps
from commons.Helpers.Helper_JsonEncoder import loads as json_loads
from commons import consts
from commons import log_utils
from commons import translation_utils
from apps.bi import model_enums
from apps.bi import worktable_utils
from apps.bi import cache_chart_utils


log = log_utils.get_logging("memorize.chart")


def get_key(obj, signature, kwargs):
    args_str_list = list()
    args_str_list.append(obj.oid)
    args_str_list.append(signature)
    tmp_kwargs = kwargs.copy()
    if tmp_kwargs.get('locale'):
        tmp_kwargs.update(dict(locale=tmp_kwargs.get('locale').code))
    args_str_list.append(dumps(tmp_kwargs))
    args_str = '#'.join([str(x) for x in args_str_list])
    return hashlib.md5(args_str.encode('utf-8')).hexdigest()


def memorize_chart(function):
    @functools.wraps(function)
    async def helper(*args, **kwargs):
        if not settings.CACHE_CHART_MODE:
            return await function(*args, **kwargs)
        else:
            chart = args[0]
            worktable = await worktable_utils.get_worktable(chart.worktable_id)
            signature = await worktable_utils.get_signature(worktable)
            key = get_key(chart, signature, kwargs)
            cached_chart = await cache_chart_utils.get_cached_chart_by_key_ttype(key, model_enums.CACHECHART_TTYPE_SHOW)
            if cached_chart is None:
                value = {"option_str": {}, "chart_option": {}}
                params = ObjectDict(
                    chart_id=chart.oid,
                    worktable_id=worktable.oid,
                    diy_name=chart.custom_attr.get("chart_type", None),
                    ttype=model_enums.CACHECHART_TTYPE_SHOW,
                    status=model_enums.CACHECHART_STATUS_UNDONE,
                    key=key,
                    value=json_dumps(value)
                )
                cached_chart_id = await cache_chart_utils.create_cachechart(params)
                cached_chart = await cache_chart_utils.get_cachechart(cached_chart_id)
            elif cached_chart.status == model_enums.CACHECHART_STATUS_SUCCESS:
                all_option = json_loads(cached_chart.value)
                return all_option.get('option_str'), all_option.get('chart_option')
            elif cached_chart.status == model_enums.CACHECHART_STATUS_UNDONE:
                raise ResourceError(AppResourceError.ChartCalcing, "该展示图表正在后端计算，请稍等后刷新!")
            elif cached_chart.status == model_enums.CACHECHART_STATUS_FAILED:
                raise ResourceError(AppResourceError.ChartFailed, "该展示图表正在后端计算，若您想立刻确认图表数据请联系管理员!")
            else:
                raise UnknownError("未定义的状态!")

            try:
                option_str, chart_option = await function(*args, **kwargs)
                params = ObjectDict(
                    status=model_enums.CACHECHART_STATUS_SUCCESS,
                    value=json_dumps({"option_str": option_str, "chart_option": chart_option})
                )
                await cache_chart_utils.update_cachechart(cached_chart.oid, params)
                return option_str, chart_option
            except Exception as e:
                params = ObjectDict(
                    status=model_enums.CACHECHART_STATUS_FAILED,
                )
                await cache_chart_utils.update_cachechart(cached_chart.oid, params)
                raise e

    return helper


def memorize_download(function):
    @functools.wraps(function)
    async def helper(*args, **kwargs):
        if not settings.CACHE_CHART_MODE:
            return await function(*args, **kwargs)
        else:
            chart = args[0]
            worktable = await worktable_utils.get_worktable(chart.worktable_id)
            signature = await worktable_utils.get_signature(worktable)
            key = get_key(chart, signature, kwargs)
            cached_chart = await cache_chart_utils.get_cached_chart_by_key_ttype(key, model_enums.CACHECHART_TTYPE_DOWNLOAD)
            if cached_chart is None:
                value = [{'headers': [], 'datas': [[]]}]
                params = ObjectDict(
                    chart_id=chart.oid,
                    worktable_id=worktable.oid,
                    diy_name=chart.custom_attr.get("chart_type", None),
                    ttype=model_enums.CACHECHART_TTYPE_SHOW,
                    status=model_enums.CACHECHART_STATUS_UNDONE,
                    key=key,
                    value=json_dumps(value)
                )
                cached_chart_id = await cache_chart_utils.create_cachechart(params)
                cached_chart = await cache_chart_utils.get_cachechart(cached_chart_id)
            elif cached_chart.status == model_enums.CACHECHART_STATUS_SUCCESS:
                return json_loads(cached_chart.value)
            elif cached_chart.status == model_enums.CACHECHART_STATUS_UNDONE:
                raise ResourceError(AppResourceError.ChartCalcing, "该下载图表正在后端计算，请稍等后重新下载!")
            elif cached_chart.status == model_enums.CACHECHART_STATUS_FAILED:
                raise ResourceError(AppResourceError.ChartFailed, "该下载图表正在后端计算，若您想立刻确认图表数据请联系管理员!")
            else:
                raise UnknownError("未定义的状态!")
            try:
                # TODO 这块逻辑感觉导致了函数的功能不单一， 需要再考虑下相关流程
                data = await function(*args, **kwargs)
                params = ObjectDict(
                    status=model_enums.CACHECHART_STATUS_SUCCESS,
                    value=json_dumps(data)
                )
                await cache_chart_utils.update_cachechart(cached_chart.oid, params)
                return data
            except Exception as e:
                params = ObjectDict(
                    status=model_enums.CACHECHART_STATUS_FAILED,
                )
                await cache_chart_utils.update_cachechart(cached_chart.oid, params)
                raise e

    return helper


def memorize_datafilter(function):
    @functools.wraps(function)
    async def helper(*args, **kwargs):
        if not settings.CACHE_CHART_MODE:
            return await function(*args, **kwargs)
        else:
            data_filter = args[0]
            worktable = await worktable_utils.get_worktable(data_filter.worktable_id)
            signature = await worktable_utils.get_signature(worktable)
            key = get_key(data_filter, signature, kwargs)
            cached_data_filter = await cache_chart_utils.get_cached_chart_by_key_ttype(key, model_enums.CACHECHART_TTYPE_DATAFILTER)
            if cached_data_filter is None:
                params = ObjectDict(
                    data_filter_id=data_filter.id,
                    worktable_id=worktable.oid,
                    diy_name=data_filter.custom_attr.get("datafilter_type", None),
                    ttype=model_enums.CACHECHART_TTYPE_DATAFILTER,
                    status=model_enums.CACHECHART_STATUS_UNDONE,
                    key=key,
                    value=json_dumps([])
                )
                cached_data_filter_id = await cache_chart_utils.create_cachechart(params)
                cached_data_filter = await cache_chart_utils.get_cachechart(cached_data_filter_id)
            elif cached_data_filter.status == model_enums.CACHECHART_STATUS_SUCCESS:
                return json_loads(cached_data_filter.value)
            elif cached_data_filter.status == model_enums.CACHECHART_STATUS_UNDONE:
                raise ResourceError(AppResourceError.ChartCalcing, "该数据筛选器正在后端计算，请稍等后刷新!")
            elif cached_data_filter.status == model_enums.CACHECHART_STATUS_FAILED:
                raise ResourceError(AppResourceError.ChartFailed, "该数据筛选器计算失败，若您想立刻确认图表数据请联系管理员!")
            else:
                raise UnknownError("未定义的状态!")
            try:
                # TODO 这块逻辑感觉导致了函数的功能不单一， 需要再考虑下相关流程
                data = await function(*args, **kwargs)
                params = ObjectDict(
                    status=model_enums.CACHECHART_STATUS_SUCCESS,
                    value=json_dumps(data)
                )
                await cache_chart_utils.update_cachechart(cached_data_filter.oid, params)
                return data
            except Exception as e:
                params = ObjectDict(
                    status=model_enums.CACHECHART_STATUS_FAILED,
                )
                await cache_chart_utils.update_cachechart(cached_data_filter.oid, params)
                raise e

    return helper
