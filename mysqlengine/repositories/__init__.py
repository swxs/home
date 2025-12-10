# -*- coding: utf-8 -*-
# @File    : repositories/__init__.py
# @AUTH    : code_creater

import os
import pathlib
from typing import TypeVar

from productor import Productor

import core.path as path

# 本模块方法
from .base import BaseRepository

T = TypeVar("T", bound=BaseRepository)

base_path = str(pathlib.Path(path.SITE_ROOT, "apps"))
repository_productor = Productor[type[BaseRepository[T]]](path.SITE_ROOT, base_path, BaseRepository, BaseRepository)
