# -*- coding: utf-8 -*-
# @File    : Helper_json.py
# @AUTH    : swxs
# @Time    : 2018/9/6 16:48

import json
import math
import datetime
import decimal
import itertools
import numpy as np
import pandas as pd

try:
    Period = pd.Period
except AttributeError:
    Period = pd._period.Period

CONVERTERS = {
    'date': lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'),
    'datetime': lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'),
    'decimal': decimal.Decimal,
}


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime,)):
            return {"val": obj.strftime('%Y-%m-%d %H:%M:%S'), "_spec_type": "datetime"}
        if isinstance(obj, (datetime.date,)):
            return {"val": obj.strftime('%Y-%m-%d'), "_spec_type": "date"}
        elif isinstance(obj, (decimal.Decimal,)):
            return {"val": str(obj), "_spec_type": "decimal"}
        else:
            return super(ComplexEncoder, self).default(obj)


def object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj

    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
            return int(obj)
        elif isinstance(obj, (np.float, np.float16, np.float32, np.float64)):
            if math.isnan(obj):
                return "N/A"
            elif np.isinf(obj):
                return "Inf"
            else:
                return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, Period):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return super(MyEncoder, self).default(obj)
