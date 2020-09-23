# -*- coding: utf-8 -*-
# @File    : Singleton.py
# @AUTH    : swxs
# @Time    : 2018/7/14 15:24


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
