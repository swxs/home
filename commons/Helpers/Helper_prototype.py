# -*- coding: utf-8 -*-
# @File    : Helper_prototype.py
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
        new_attrs = dict()
        __value__ = ObjectDict()

        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell

        for key, value in copy.copy(attrs).items():
            if key.startswith("__"):
                new_attrs[key] = value
            else:
                __value__[key] = value
        new_attrs["__value__"] = __value__
        return super(__Proto__, mcs).__new__(mcs, name, bases, new_attrs)


class Prototype(object, metaclass=__Proto__):
    """
    主要用来实现属性的拼装
    class类定义的属性是原型，记录在__value__中，可以通过类型注解指定属性的配置key
    类的实例化时会复制原型定义的属性，可以在此时对复制出的属性做修改，也可以后续动态修改
    类的实例可以被调用，会尝试迭代将包含类型注解的属性替换成配置值
    """

    def __init__(self, **kwargs):
        self.__dict__ = copy.deepcopy(self.__value__)
        self.__dict__.update(**kwargs)
        super(Prototype, self).__init__()

    def __call__(self, **kwargs):
        new_element = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                new_element[key] = [v(**kwargs) if isinstance(v, Prototype) else v for v in value]
            else:
                if isinstance(value, Prototype):
                    new_element[key] = value(**kwargs)
                else:
                    if key in getattr(self, "__annotations__", {}):
                        new_element[key] = kwargs.get(self.__annotations__.get(key), value)
                    else:
                        new_element[key] = value
        self.__dict__ = new_element
        return self

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
