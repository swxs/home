# -*- coding: utf-8 -*-
# @File    : manager_sqlalchemy.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio
import logging
from collections import defaultdict
from typing import List

import pymysql
from sqlalchemy import and_, create_engine, desc, func, not_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import schema
from sqlalchemy_aio import ASYNCIO_STRATEGY

import core

# 通用方法
from commons.Metaclass.Singleton import Singleton

# 本模块方法
from ..fields import DictField
from .manager_base import BaseManager, BaseManagerQuerySet

logger = logging.getLogger("main.dao.manager.manager_sqlalchemy")


NAME_DICT = defaultdict(dict)

Base = declarative_base()


class Ix:
    def __new__(cls, keys: List[str] = [], unique: bool = False, name: str = None):
        name = cls._get_ix_prefix(*keys, unique=unique, name=name)
        if unique:
            return schema.UniqueConstraint(*keys, name=name)
        else:
            return schema.Index(name, *keys)

    @classmethod
    def _get_ix_prefix(cls, *keys, unique: bool = False, name: str = None):
        pattern = {True: "uix_" + "_".join(keys).lower(), False: "ix_" + "_".join(keys).lower()}
        if not name:
            return pattern.get(unique is True)
        else:
            return name


expression_dict = {
    'or_': or_,
    'and_': and_,
}


def params_to_query(model_class: Base, params: dict, as_query=True):
    """
    根据传入的dict类型参数条件进行 query查询语句的转换
    """
    query_list = []
    for k, v in params.items():
        # if expression_dict.get(k):
        # query_list.append(expression_dict.get(k)(params_to_query(model_class, v)))
        if k in expression_dict:
            if isinstance(v, list):
                express_list = []
                for ele in v:
                    express_list.append(params_to_query(model_class, ele))
                query_list.append(expression_dict[k](*express_list))
            else:
                query_list.append(expression_dict[k](*params_to_query(model_class, v, False)))
        if not hasattr(model_class, k):
            continue
        elif isinstance(v, list):
            query_list.append(getattr(model_class, k).in_(v))
        else:
            query_list.append(getattr(model_class, k) == v)

    if as_query:
        return and_(*query_list)
    return query_list


class SqlalchemyConnector(object, metaclass=Singleton):
    engine = None
    Session = None

    def initialize(self):
        logging.info("connect to mysql database....")
        pymysql.install_as_MySQLdb()
        if self.engine is None:
            URL = f'mysql+pymysql://root:C3f0a217f50e@{core.config.DB_HOST}:{core.config.DB_PORT}/{core.config.DB_NAME}'
            logging.info(f"URL: {URL}")
            self.engine = create_engine(
                URL,
                # strategy=ASYNCIO_STRATEGY,
                echo=False,
            )

        if self.Session is None:
            self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        logging.info(f"{Base.metadata}")
        Base.metadata.create_all(bind=self.engine)
        logging.info(f"Connected to mysql database!")

    def finish(self):
        pass


class ManagerQuerySet(BaseManagerQuerySet):
    pass


class SqlalchemyManager(BaseManager, metaclass=Singleton):
    name = "sqlalchemy"

    def __init__(self, dao):
        super().__init__(dao)
        self.connector = SqlalchemyConnector()
        self.connector.initialize()

    def get_instance(self, model):
        if model is None:
            return None
        data = dict()
        for attr in getattr(self.dao, "__fields__"):
            data[attr] = getattr(model, attr)
        data["id"] = getattr(model, "id")
        return self.dao(**data)

    async def count(self, finds):
        db = self.connector.Session()
        try:
            return await db.query(self.model).filter(finds)
        except Exception as e:
            logging.exception(f"count failed! finds = {finds}")
            return None
        finally:
            db.close()

    async def find_one(self, finds):
        db = self.connector.Session()
        try:
            querys = params_to_query(self.model, finds)
            # return await db.query(self.model).filter(querys).first()
            return db.query(self.model).filter(querys).first()
        except Exception as e:
            logging.exception(f"find_one failed! finds = {finds}")
            return None
        finally:
            db.close()

    async def find_many(self, finds, limit=0, skip=0):
        db = self.connector.Session()
        try:
            cursor = await db.query(self.model).filter(finds).offset(skip).limit(limit).all()
            return ManagerQuerySet(self.get_instance, cursor)
        except Exception as e:
            logging.exception(f"find_many failed! finds = {finds}")
            return []
        finally:
            db.close()

    async def create(self, params):
        db = self.connector.Session()
        try:
            model = self.model()
            for __field_name, __field in getattr(self.dao, "__fields__").items():
                v = params.get(__field_name, __field.create_default)
                if v is not None:
                    setattr(model, __field_name, v)
            db.add(model)
            db.commit()
            db.refresh(model)
            return self.get_instance(model)
        except Exception as e:
            logging.exception(f"create failed! params = {params}")
            return None

    async def update_one(self, finds, params):
        db = self.connector.Session()
        try:
            model = await self.model.find_one(finds)
            for __field_name, __field in getattr(self.dao, "__fields__").items():
                if __field._default_update:
                    setattr(model, __field_name, __field.update_default)
                if __field_name in params:
                    setattr(model, __field_name, params.get(__field_name))
            await model.commit()
            return self.get_instance(model)
        except Exception as e:
            logging.exception(f"update_one failed! finds = {finds}, params = {params}")
            return None

    async def delete_one(self, finds):
        try:
            model = await self.model.find_one(finds)
            delete_result = await model.delete()
            return delete_result.deleted_count
        except Exception as e:
            logging.exception(f"delete_one failed! finds = {finds}")
            return 0
