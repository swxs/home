# -*- coding: utf-8 -*-
# @File    : result.py
# @AUTH    : swxs
# @Time    : 2019/9/20 15:06

import json


class ResultData(object):
    """
    数据结果
    """

    def __init__(self, code=0, msg=None, **kwargs):
        self.code = code
        self.msg = msg
        self.kwargs = kwargs

    @property
    def data(self):
        result = {}
        result.update(vars(self))
        result.update(self.kwargs)
        result.__delitem__('kwargs')
        return result

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)

    def to_json(self):
        return json.dumps(self.data)

    def to_thrift(self, thrift):
        result = thrift()
        result.code = self.code
        result.msg = self.msg
        if "data" in self.kwargs:
            result.data = self.kwargs.get("data")
        return result


class ExceptionData(ResultData):
    """
    异常返回的结果
    """

    def __init__(self, e):
        super(ExceptionData, self).__init__(code=e.code, msg=e.message)


class SuccessData(ResultData):
    """
    成功返回的结果
    """

    def __init__(self, data, **kwargs):
        kwargs.update({'data': data})
        super(SuccessData, self).__init__(code=0, data=kwargs)

    def __setitem__(self, key, value):
        self.kwargs['data'][key] = value