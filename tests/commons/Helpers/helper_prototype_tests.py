# -*- coding: utf-8 -*-
# @File    : helper_prototype_tests.py
# @AUTH    : swxs
# @Time    : 2018/11/27 17:57

import time
import math
import unittest
from commons.Helper.Helper_prototype import Prototype


class A(Prototype):
    name = "a"
    value = []


class B(Prototype):
    name = "b"
    value = []


class C(Prototype):
    name = "c"
    value = [A(), B()]


class SingletonHelperTestCase(unittest.TestCase):
    def test_proto_single(self):
        """
        可以正确的创建指定对象
        :return:
        """
        a = A()
        self.assertEqual(a.name, "a")

    def test_proto_single_change(self):
        """
        创建的对象可以修改指定属性
        :return:
        """
        a1 = A(name="a1")
        a2 = A(name="a2")
        a3 = A()
        self.assertEqual(a1.name, "a1")
        self.assertEqual(a2.name, "a2")
        self.assertEqual(a3.name, "a")

    def test_proto_single_change2(self):
        """
        创建的对象可以修改引用属性
        :return:
        """
        a1 = A(value=[A(name="a1")])
        a2 = A(value=[A(name="a2")])
        a3 = A()
        self.assertEqual(a1.value[0].name, "a1")
        self.assertEqual(a2.value[0].name, "a2")
        self.assertEqual(a3.value, [])

    def test_proto_single_change3(self):
        """
        创建的对象可以修改引用属性
        :return:
        """
        a1 = A(value=[A(name="a1")])
        a2 = A()
        a1.value.append(A(name="a2")())
        self.assertEqual(a1.value[0].name, "a1")
        self.assertEqual(a1.value[1].name, "a2")
        self.assertEqual(a2.value, [])

    def test_proto_parent(self):
        c = C()
        self.assertEqual(c.value[0].name, "a")

    def test_proto_parent_change(self):
        c1 = C(value=[A(name="a1")])
        c2 = C()
        self.assertEqual(c1.value[0].name, "a1")
        self.assertEqual(c2.value[0].name, "a")
        self.assertEqual(len(c1.value), 1)

    def test_proto_call(self):
        """
        对对象的调用会返回一个ObjecDict, 包含所有属性
        :return:
        """
        a = A()
        self.assertEqual(a().name, "a")

    def test_proto_call_after_change(self):
        """
        对对象的修改， 会作用到调用返回的ObjecDict上
        :return:
        """
        a = A()
        a.name = "b"
        self.assertEqual(a().name, "b")
