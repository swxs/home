# -*- coding: utf-8 -*-
# @File    : MemorizeChart.py
# @AUTH    : swxs
# @Time    : 2018/9/11 10:03

import hashlib
import functools
import json
import traceback

from apps.consts import const
from apps.consts.bi import data_filter as data_filter_consts
from apps.consts.bi import cached_chart as cached_chart_consts
from apps.utils.bi.cached_chart import CachedChart
from common.Decorator import MemorizeFile
from common.ApiExceptions import CommonException, NoDataException
from common.Utils import utils, translation
from common.Utils.log_utils import getLogger

log = getLogger("memorize.chart")


def get_key(obj, kwargs):
    args_str_list = list()
    args_str_list.append(obj.oid)
    tmp_kwargs = kwargs.copy()
    if tmp_kwargs.get('locale'):
        tmp_kwargs.update(dict(locale=tmp_kwargs.get('locale').code))
    args_str_list.append(utils.serialize(tmp_kwargs))
    args_str = '#'.join([str(x) for x in args_str_list])
    return hashlib.md5(args_str.encode('utf-8')).hexdigest()


def remove_data_of_worktable_id(worktable_id):
    from apps.utils.bi.chart_page import ChartPage
    MemorizeFile.remove_data_memorize_by_worktable_id(worktable_id)
    chart_page_list = ChartPage.get_chart_page_list_by_worktable_id(worktable_id)
    for chart_page in chart_page_list:
        # chart_page.worktable.get_dataframe()
        CachedChart.delete_cached_chart_by_chart_page_id(chart_page.oid)


def memorize_chartpage(function):
    @functools.wraps(function)
    def helper(*args, **kwargs):
        chart_page = args[0]
        key = get_key(chart_page, kwargs)
        cached_chart_page = CachedChart.get_cached_chart_by_key_ttype(key, cached_chart_consts.CHARTPAGE)
        if cached_chart_page is None:
            function(*args, **kwargs)
            CachedChart.create(chart_page_id=chart_page.oid, ttype=cached_chart_consts.CHARTPAGE, status=cached_chart_consts.STATUS_SUCCESS, key=key)

    return helper


def memorize_chart(function):
    @functools.wraps(function)
    def helper(*args, **kwargs):
        from apps.utils.bi.chart_page import ChartPage
        chart = args[0]
        key = get_key(chart, kwargs)
        cached_chart = CachedChart.get_cached_chart_by_key_ttype(key, cached_chart_consts.SHOW)
        if cached_chart is None:
            chart_page = ChartPage.get_chart_page_by_chart_id(chart.oid)
            value = {"option_str": {}, "chart_option": {}}
            cached_chart = CachedChart.create(chart_id=chart.oid,
                                              chart_page_id=chart_page.oid,
                                              ttype=cached_chart_consts.SHOW,
                                              status=cached_chart_consts.STATUS_UNDONE,
                                              key=key,
                                              value=json.dumps(value))
        elif cached_chart.status == cached_chart_consts.STATUS_SUCCESS:
            all_option = json.loads(cached_chart.value)
            return all_option.get('option_str'), all_option.get('chart_option')
        elif cached_chart.status == cached_chart_consts.STATUS_UNDONE:
            raise CommonException("该展示图表正在后端计算，请稍等后刷新!")
        elif cached_chart.status == cached_chart_consts.STATUS_FAILED:
            raise CommonException("该展示图表正在后端计算，若您想立刻确认图表数据请联系管理员!")
        else:
            raise CommonException("未定义的状态!")
        try:
            option_str, chart_option = function(*args, **kwargs)
            cached_chart.update(status=cached_chart_consts.STATUS_SUCCESS, value=json.dumps({"option_str": option_str, "chart_option": chart_option}))
            return option_str, chart_option
        except:
            log.exception("memorize_chart")
            cached_chart.update(status=cached_chart_consts.STATUS_FAILED)
            return {}, {}

    return helper


def memorize_download(function):
    @functools.wraps(function)
    def helper(*args, **kwargs):
        from apps.utils.bi.chart_page import ChartPage
        chart = args[0]
        key = get_key(chart, kwargs)
        cached_chart = CachedChart.get_cached_chart_by_key_ttype(key, cached_chart_consts.DOWNLOAD)
        if cached_chart is None:
            chart_page = ChartPage.get_chart_page_by_chart_id(chart.oid)
            value = [{'headers': [], 'datas': [[]]}]
            cached_chart = CachedChart.create(chart_id=chart.oid,
                                              chart_page_id=chart_page.oid,
                                              ttype=cached_chart_consts.DOWNLOAD,
                                              key=key,
                                              status=cached_chart_consts.STATUS_UNDONE,
                                              value=json.dumps(value))
        elif cached_chart.status == cached_chart_consts.STATUS_SUCCESS:
            return json.loads(cached_chart.value)
        elif cached_chart.status == cached_chart_consts.STATUS_UNDONE:
            raise CommonException("该下载图表正在后端计算，请稍等后重新下载!")
        elif cached_chart.status == cached_chart_consts.STATUS_FAILED:
            raise CommonException("该下载图表正在后端计算，若您想立刻确认图表数据请联系管理员!")
        else:
            raise CommonException("未定义的状态!")
        try:
            data = function(*args, **kwargs)
            cached_chart.update(status=cached_chart_consts.STATUS_SUCCESS, value=json.dumps(data))
            return data
        except:
            log.exception("memorize_download")
            cached_chart.update(status=cached_chart_consts.STATUS_FAILED)
            return [{'headers': [], 'datas': [[]]}]

    return helper


def memorize_datafilter(function):
    @functools.wraps(function)
    def helper(*args, **kwargs):
        from apps.utils.bi.chart import Chart
        from apps.utils.bi.chart_page import ChartPage
        data_filter = args[0]
        key = get_key(data_filter, kwargs)
        cached_data_filter = CachedChart.get_cached_chart_by_key_ttype(key, cached_chart_consts.DATAFILTER)
        if cached_data_filter is None:
            if data_filter.ttype == data_filter_consts.TTYPE_CHART:
                chart = Chart.get_chart_by_data_filter_id(data_filter.oid)
                chart_page = ChartPage.get_chart_page_by_chart_id(chart.oid)
                cached_data_filter = CachedChart.create(chart_id=chart.oid,
                                                        chart_page_id=chart_page.oid,
                                                        data_filter_id=data_filter.oid,
                                                        ttype=cached_chart_consts.DATAFILTER,
                                                        key=key,
                                                        status=cached_chart_consts.STATUS_UNDONE,
                                                        value=json.dumps([]))
            elif data_filter.ttype == data_filter_consts.TTYPE_CHARTPAGE:
                chart_page = ChartPage.get_chart_page_by_data_filter_id(data_filter.oid)
                cached_data_filter = CachedChart.create(chart_page_id=chart_page.oid,
                                                        data_filter_id=data_filter.oid,
                                                        ttype=cached_chart_consts.DATAFILTER,
                                                        key=key,
                                                        status=cached_chart_consts.STATUS_UNDONE,
                                                        value=json.dumps([]))
            else:
                raise CommonException("未定义的筛选器类型!")
        elif cached_data_filter.status == cached_chart_consts.STATUS_SUCCESS:
            return json.loads(cached_data_filter.value)
        elif cached_data_filter.status == cached_chart_consts.STATUS_UNDONE:
            raise CommonException("该数据筛选器正在后端计算，请稍等后刷新!")
        elif cached_data_filter.status == cached_chart_consts.STATUS_FAILED:
            raise CommonException("该数据筛选器计算失败，若您想立刻确认图表数据请联系管理员!")
        else:
            raise CommonException("未定义的状态!")
        try:
            data = function(*args, **kwargs)
            cached_data_filter.update(status=cached_chart_consts.STATUS_SUCCESS, value=json.dumps(data))
            return data
        except NoDataException as e:
            if kwargs.get('locale'):
                _, code = translation.get_translate_and_code(kwargs.get('locale'))
                data = [{const.BASE_LOCALE: '全部', kwargs.get('locale').code: _('全部')}, ]
            else:
                data = ['全部', ]
            cached_data_filter.update(status=cached_chart_consts.STATUS_SUCCESS, value=json.dumps(data))
            return data
        except:
            log.exception("memorize_datafilter")
            cached_data_filter.update(status=cached_chart_consts.STATUS_FAILED)
            if kwargs.get('locale'):
                _, code = translation.get_translate_and_code(kwargs.get('locale'))
                return [{const.BASE_LOCALE: '全部', kwargs.get('locale').code: _('全部')}, ]
            else:
                return ['全部', ]

    return helper
