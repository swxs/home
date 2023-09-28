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

base_path = os.path.dirname(os.path.abspath(__file__))
content_productor = Productor(core.path.SITE_ROOT, base_path, Content, Content, "*.py")
