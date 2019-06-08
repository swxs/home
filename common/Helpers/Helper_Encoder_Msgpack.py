# -*- coding: utf-8 -*-
# @File    : Helper_Encoder_Msgpack.py
# @AUTH    : swxs
# @Time    : 2019/1/17 17:21

import msgpack
from functools import partial
from .Helper_Encoder import (CONVERTERS, encoder)

__all__ = ["dumps", "loads", ]


def default(obj):
    try:
        encoded_object = encoder(obj)
        return msgpack.ExtType(encoded_object["_spec_type"], bytes(encoded_object["val"], "utf8"))
    except Exception as e:
        raise TypeError("Unknown type: %r" % (obj,))


def ext_hook(code, data):
    if code in CONVERTERS:
        return CONVERTERS[code](data.decode("utf8"))
    return msgpack.ExtType(code, data)


dumps = partial(msgpack.packb, default=default, use_bin_type=True)
loads = partial(msgpack.unpackb, ext_hook=ext_hook)
