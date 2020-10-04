# -*- coding: utf-8 -*-
# @File    : filter_result.py
# @AUTH    : swxs
# @Time    : 2019/9/23 15:08

import functools
import collections


def __do_filter(result, filter):
    if len(filter) == 1:
        if filter[0] in result:
            result.pop(filter[0])
        return result
    else:
        checked = result.get(filter[0])
        if isinstance(checked, dict):
            result[filter[0]] = __do_filter(checked, filter[1:])
        elif isinstance(checked, list):
            result[filter[0]] = [__do_filter(new_result, filter[1:]) for new_result in checked]
        return result


def __filter_result(request, result):
    if isinstance(result, dict):
        filters = request.get_query_argument("filters", "").split("|")
        for filter in filters:
            f = filter.split(".")
            result = __do_filter(result, f)
    return result


def do_filter(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        result_data = func(self, *args, **kwargs)
        if isinstance(result_data, collections.Awaitable):
            result_data = await result_data
        return __filter_result(self.request, result_data)

    return wrapper
