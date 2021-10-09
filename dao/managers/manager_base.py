# -*- coding: utf-8 -*-
# @File    : manager_base.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio


class BaseManagerQuerySet(object):
    def __init__(self, get_instance, cursor):
        """
        :param get_instance: 转换为对应类的方法
        :param cursor: cursor
        """
        self.get_instance = get_instance
        self.cursor = cursor
        self.filters = dict()

    def __iter__(self):
        """
        简介
        ----------
        迭代器

        """

    def __next__(self, cursor):
        """
        简介
        ----------
        应该在此处包装原始model

        参数
        ----------
        cursor :

        """

    async def __aiter__(self):
        """
        简介
        ----------
        异步迭代器

        """

    async def __anext__(self):
        """
        简介
        ----------
        应该在此处包装原始model

        """

    async def first(self):
        """
        简介
        ----------
        获取第一个对象，并包装

        """

    def order_by(self, keys):
        """
        简介
        ----------
        排序对象


        返回
        -------

        """


class BaseManager(object):
    def __init__(self, dao) -> None:
        super().__init__()
        self.dao = dao
        self.model = dao.__model__

    async def find_one(self, finds, limit=0, skip=0):
        pass

    async def find_many(self, finds, limit=0, skip=0):
        pass

    async def count(self, finds):
        pass

    async def create(self, params):
        pass

    async def find_one_and_update(self, finds, params):
        pass

    async def find_one_and_delete(self, finds):
        pass
