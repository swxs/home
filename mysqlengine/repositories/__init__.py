# -*- coding: utf-8 -*-
# @File    : repositories/__init__.py
# @AUTH    : code_creater

import os
import pathlib

from productor import Productor

import core.path as path

# 本模块方法
from .base import BaseRepository

base_path = str(pathlib.Path(path.SITE_ROOT, "apps"))
repository_productor = Productor(path.SITE_ROOT, base_path, BaseRepository, BaseRepository)
