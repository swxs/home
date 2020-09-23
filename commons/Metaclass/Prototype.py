# -*- coding: utf-8 -*-
# @File    : Prototype.py
# @AUTH    : swxs
# @Time    : 2019/2/27 15:22

import copy
from tornado.util import ObjectDict


class __Proto__(type):
    def __new__(mcs, name, bases, attrs):
        """
        __value__字段用来记录该原型的相关信息
        :param name:
        :param bases:
        :param attrs:
        :return:
        """
        __value__ = dict()
        for key, value in attrs.items():
            if not key.startswith("_") and (key != "clone"):
                if isinstance(value, list):
                    __value__[key] = [v() if isinstance(v, Prototype) else v for v in value]
                elif isinstance(value, Prototype):
                    __value__[key] = value()
                else:
                    __value__[key] = value
        for key, value in __value__.items():
            attrs.pop(key)
        attrs["__value__"] = __value__
        return super(__Proto__, mcs).__new__(mcs, name, bases, attrs)


class Prototype(object, metaclass=__Proto__):
    """
    主要用来实现属性的拼装， 性质看对应测试用例
    有三个环节：
    定义的class类是原型，其属性记录在__value__中
    类的实例化时引用原型，可以在此时对原型做相应修改，也可以在后续逻辑中通过clone修改
    类的实例可以被调用，返回一个包含类所有属性的ObjectDict（可以做临时修改）, 该字典的修改与类的实例相互独立
    """

    def __init__(self, **kwargs):
        self.__dict__ = ObjectDict(self.__value__)
        self._update(self.__dict__, **kwargs)
        super(Prototype, self).__init__()

    def __call__(self, **kwargs):
        copyed = copy.deepcopy(self.__dict__)
        self._update(copyed, **kwargs)
        return copyed

    def _update(self, base_dict, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, list):
                base_dict.update({key: [v() if isinstance(v, Prototype) else v for v in value]})
            elif isinstance(value, Prototype):
                base_dict.update({key: value()})
            else:
                base_dict.update({key: value})

    def clone(self, **kwargs):
        self._update(self.__dict__, **kwargs)
        return self
