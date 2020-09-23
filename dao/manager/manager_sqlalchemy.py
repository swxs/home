# -*- coding: utf-8 -*-
# @File    : manager_sqlalchemy.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio
from collections import defaultdict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, MetaData, Table
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker


import settings
from web.consts import undefined
from web.exceptions import ApiException, Info
from ..fields import DictField
from .manager_base import BaseManager, BaseManagerQuerySet
from commons.Metaclass.Singleton import Singleton
from commons.Utils.log_utils import getLogger

log = getLogger("manager.manager_sqlalchemy")

Base = declarative_base()
NAME_DICT = defaultdict(dict)


class ManagerQuerySet(BaseManagerQuerySet):
    pass


class Manager(BaseManager, metaclass=Singleton):
    name = "sqlalchemy"
    Session = sessionmaker(bind=settings.engine)

    @classmethod
    def _get_model(cls, klass):
        return NAME_DICT[cls.name][klass.__name__]
