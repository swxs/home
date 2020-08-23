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
    name = "base"

    @classmethod
    def _get_model(cls, klass):
        return cls._get_model(klass)

    @classmethod
    def search(cls, klass, searches, limit=0, skip=0):
        """
        简介
        ----------
        选择获取一些满足条件的对象，并返回一个QuerySet对象

        参数
        ----------
        klass :

        searches :

        """

    @classmethod
    async def count(cls, klass, searches):
        """
        简介
        ----------
        获取满足筛选条件的对象数量

        参数
        ----------
        klass :

        searches :

        """

    @classmethod
    async def find(cls, klass, finds):
        """
        简介
        ----------
        选择获取一个满足条件的对象实例，并初始化

        参数
        ----------
        klass :

        finds :

        """

    @classmethod
    async def create(cls, klass, creates):
        """
        简介
        ----------
        创建一个对象实例，并初始化

        参数
        ----------
        klass :

        creates :

        """

    @classmethod
    async def update(cls, klass, instance, updates):
        """
        简介
        ----------
        更新一个对象实例，并返回

        参数
        ----------
        klass :

        instance :

        updates :

        """

    @classmethod
    async def find_and_update(cls, klass, finds, updates):
        """
        简介
        ----------
        更新一个对象实例，并返回

        参数
        ----------
        klass :

        finds :

        updates :

        """

    @classmethod
    async def delete(cls, klass, instance):
        """
        简介
        ----------
        删除一个对象实例

        参数
        ----------
        klass :

        instance :

        """

    @classmethod
    async def find_and_delete(cls, klass, finds):
        """
        简介
        ----------
        删除一个对象实例

        参数
        ----------
        klass :

        finds :

        """

    @classmethod
    async def search_and_delete(cls, klass, searches):
        """
        简介
        ----------
        删除一个对象实例

        参数
        ----------
        klass :

        searches :

        """
