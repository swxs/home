# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @AUTH    : swxs
# @Time    : 2019/2/26 15:07

import os
import sys

import core

# 通用方法
from commons.Helpers.Helper_productor import Productor

# 本模块方法
from .content import Content


class ContentProductor(Productor):
    def __init__(
        self,
        root_dir: str,
        start_dir: str,
        base_module: object = None,
        temp_module: object = None,
        pattern: str = '*.py',
    ):
        super().__init__(root_dir, start_dir, base_module=base_module, temp_module=temp_module, pattern=pattern)


base_path = os.path.dirname(os.path.abspath(__file__))
content_productor = ContentProductor(core.path.SITE_ROOT, base_path, Content, Content, "*.py")
