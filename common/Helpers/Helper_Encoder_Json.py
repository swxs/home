# -*- coding: utf-8 -*-
# @File    : Helper_Encoder_Json.py
# @AUTH    : swxs
# @Time    : 2018/5/16 9:56

import json
from functools import partial
from .Helper_Encoder import (CONVERTERS, encoder)

__all__ = ["dump", "dumps", "load", "loads", ]


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return encoder(obj)
        except Exception:
            return super(ComplexEncoder, self).default(obj)


def json_object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj

    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))


dump = partial(json.dump, cls=ComplexEncoder)
dumps = partial(json.dumps, cls=ComplexEncoder)
load = partial(json.load, object_hook=json_object_hook)
loads = partial(json.loads, object_hook=json_object_hook)
