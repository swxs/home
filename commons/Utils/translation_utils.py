# -*- coding: utf-8 -*-
# File    : translation.py.py
# Author  : gorden
# Time    : 2018/8/24 17:30


import settings


def get_translate_and_code(locale):
    if locale:
        return locale.translate, locale.code
    else:
        return lambda x: x, settings.DEFAULT_LOCAL
