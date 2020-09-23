# -*- coding: utf-8 -*-
# @File    : Helper_Encoder.py
# @AUTH    : swxs
# @Time    : 2019/1/17 17:23

import datetime
import decimal
import math
import numpy as np
import pandas as pd

try:
    Period = pd.Period
except AttributeError:
    Period = pd._period.Period


from bson import ObjectId

CONVERTERS_TYPE_DATE = 42  # date
CONVERTERS_TYPE_DATETIME = 43  # datetime
CONVERTERS_TYPE_DECIMAL = 44  # decimal
CONVERTERS_TYPE_UNDEFINED = 45
CONVERTERS_TYPE_OBJECTFIELD = 46

CONVERTERS = {
    CONVERTERS_TYPE_DATE: lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'),
    CONVERTERS_TYPE_DATETIME: lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'),
    CONVERTERS_TYPE_DECIMAL: decimal.Decimal,
    CONVERTERS_TYPE_OBJECTFIELD: lambda x: ObjectId(x),
}


def encoder(obj):
    if isinstance(obj, (datetime.datetime,)):
        return {"val": obj.strftime('%Y-%m-%d %H:%M:%S'), "_spec_type": CONVERTERS_TYPE_DATETIME}
    elif isinstance(obj, (datetime.date,)):
        return {"val": obj.strftime('%Y-%m-%d'), "_spec_type": CONVERTERS_TYPE_DATE}
    elif isinstance(obj, (decimal.Decimal,)):
        return {"val": str(obj), "_spec_type": CONVERTERS_TYPE_DECIMAL}
    elif isinstance(obj, (ObjectId,)):
        return {"val": str(obj), "_spec_type": CONVERTERS_TYPE_OBJECTFIELD}
    elif isinstance(obj, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
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
    else:
        raise Exception("Not NotImplemented")


def object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj

    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))
