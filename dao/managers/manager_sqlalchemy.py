# -*- coding: utf-8 -*-
# @File    : manager_sqlalchemy.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio
import logging
from collections import defaultdict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, MetaData, Table
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker


from core import config
from commons.Metaclass.Singleton import Singleton
from ..fields import DictField
from .manager_base import BaseManager, BaseManagerQuerySet

logger = logging.getLogger("main.dao.manager.manager_sqlalchemy")

Base = declarative_base()
NAME_DICT = defaultdict(dict)


class ManagerQuerySet(BaseManagerQuerySet):
    pass


class SqlalchemyManager(BaseManager, metaclass=Singleton):
    name = "sqlalchemy"
    # Session = sessionmaker(bind=config.MYSQL_INSTANCE)

    @classmethod
    def _get_model(cls, klass):
        return NAME_DICT[cls.name][klass.__name__]
