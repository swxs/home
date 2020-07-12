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
        self._filter = dict()

    def __iter__(self):
        """
        迭代器
        :return:
        """

    def __next__(self, cursor):
        """
        应该在此处包装原始model
        :return:
        """

    async def __aiter__(self):
        """
        异步迭代器
        :return:
        """

    async def __anext__(self, cursor):
        """
        应该在此处包装原始model
        :return:
        """

    async def first(self):
        """
        获取第一个对象，并包装
        :return:
        """

    def order_by(self, **kwargs):
        """
        排序对象
        :return：
        """


class BaseManager(object):
    name = "base"

    @classmethod
    def _get_model(cls, klass):
        return cls._get_model(klass)

    @classmethod
    def filter(cls, klass, **kwargs):
        """
        选择获取一些满足条件的对象，并返回一个QuerySet对象
        :param klass:
        :param kwargs:
        :return:
        """

    @classmethod
    async def count(cls, klass, **kwargs):
        """
        获取满足筛选条件的对象数量
        :param klass:
        :param kwargs:
        :return:
        """

    @classmethod
    async def select(cls, klass, **kwargs):
        """
        选择获取一个满足条件的对象实例，并初始化
        :param klass:
        :param kwargs:
        :return:
        """

    @classmethod
    async def create(cls, klass, **kwargs):
        """
        创建一个对象实例，并初始化
        :param klass:
        :param kwargs:
        :return:
        """

    @classmethod
    async def update(cls, klass, instance, **kwargs):
        """
        更新一个对象实例，并返回
        :param klass: 对象类
        :param instance: 对象实例
        :param kwargs: 更新内容
        :return:
        """

    @classmethod
    async def delete(cls, klass, instance):
        """
        删除一个对象实例
        :param klass: 对象类
        :param instance: 对象实例
        :return:
        """
