# -*- coding: utf-8 -*-
# @File    : manager_sqlalchemy.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio
import logging
from collections import defaultdict

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from core import config

# 通用方法
from commons.Metaclass.Singleton import Singleton

# 本模块方法
from ..fields import DictField
from .manager_base import BaseManager, BaseManagerQuerySet

logger = logging.getLogger("main.dao.manager.manager_sqlalchemy")


NAME_DICT = defaultdict(dict)


class ManagerQuerySet(BaseManagerQuerySet):
    pass


class SqlalchemyManager(BaseManager, metaclass=Singleton):
    name = "sqlalchemy"

    def __init__(self, dao):
        super(SqlalchemyManager, self).__init__(dao)
        pymysql.install_as_MySQLdb()
        self.base = declarative_base()
        self.engine = create_engine(
            "mysql://root:swxs@localhost/runoob",
            encoding='latin1',
            echo=False,
        )

    @classmethod
    def _get_model(cls, klass):
        return NAME_DICT[cls.name][klass.__name__]
