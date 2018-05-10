# -*- coding: utf-8 -*-
# @File    : proto_tests.py
# @AUTH    : swxs
# @Time    : 2018/5/9 14:42

import unittest
from tests import addressbook_pb2


class ProtoTestCase(unittest.TestCase):
    """
    安装 protoc ：Protoc下载地址[https://github.com/google/protobuf/releases]，可以根据自己的系统下载相应的 protoc，windows 用户统一下载 win32 版本。
    配置 protoc 到系统的环境变量中，执行如下命令查看是否安装成功：
    $ protoc --version
    如果正常打印 libprotoc 的版本信息就表明 protoc 安装成功

    安装 ProtoBuf 相关的 python 依赖库
    $ pip install protobuf
    """

    def test_set(self):
        addressbook = addressbook_pb2.AddressBook()
        person_1 = addressbook.person.add()
        person_1.id = 1
        person_1.name = "swxs"
        phone_1 = person_1.phone.add()
        phone_1.number = "13456789"
        phone_1.type = 2
        assert len(addressbook.person) == 1


