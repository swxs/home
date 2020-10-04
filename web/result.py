# -*- coding: utf-8 -*-
# @File    : result.py
# @AUTH    : swxs
# @Time    : 2019/9/20 15:06


import json
import datetime
from bson import ObjectId


def encoder(obj):
    if isinstance(obj, (datetime.datetime,)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, (datetime.date,)):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, (ObjectId,)):
        return str(obj)
    else:
        raise Exception("Not NotImplemented")


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return encoder(obj)
        except Exception:
            return super(ComplexEncoder, self).default(obj)


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
        return json.dumps(self.data, cls=ComplexEncoder)

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
        super(ExceptionData, self).__init__(code=e.code, msg=str(e))


class SuccessData(ResultData):
    """
    成功返回的结果
    """

    def __init__(self, **kwargs):
        super(SuccessData, self).__init__(code=0, data=kwargs)

    def __setitem__(self, key, value):
        self.kwargs['data'][key] = value
