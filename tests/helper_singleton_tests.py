# -*- coding: utf-8 -*-
# @File    : helper_singleton_tests.py
# @AUTH    : swxs
# @Time    : 2018/7/18 15:51

import time
import math
import unittest
from common.Metaclass.Singleton import Singleton


class A(object, metaclass=Singleton):
    """
    这种形式的单例只能触发一次__new__, __init__
    """

    def __new__(cls, value):
        cls.new_value = value
        return super(A, cls).__new__(cls)

    def __init__(self, value):
        self.value = value

    def get_value(self):
        if "value" in self.__dict__:
            return self.value
        else:
            return "No value"


class B(object):
    def __new__(cls, *args):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.__singleton__ = singleton = super(B, cls).__new__(cls)
        return singleton

    def __init__(self, value):
        self.value = value

    def get_value(self):
        if "value" in self.__dict__:
            return self.value
        else:
            return "No value"


class SingletonHelperTestCase(unittest.TestCase):
    def test_metaclass_singleton(self):
        a = A("qwe")
        self.assertEqual(a.get_value(), "qwe")
        b = A("asd")
        self.assertEqual(a.get_value(), "qwe")
        self.assertEqual(b.get_value(), "qwe")
        self.assertIs(a, b)
        self.assertEqual(id(a), id(b))

    def test_newer_singleton(self):
        a = B("qwe")
        self.assertEqual(a.get_value(), "qwe")
        b = B("asd")
        self.assertEqual(a.get_value(), "asd")
        self.assertEqual(b.get_value(), "asd")
        self.assertIs(a, b)
        self.assertEqual(id(a), id(b))
