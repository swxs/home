# -*- coding: utf-8 -*-
# @File    : fields.py
# @AUTH    : Gorden
# @Time    : 2021/9/15 01:04
import codecs

import sqlalchemy
from bson import ObjectId
from sqlalchemy import TypeDecorator


class ObjectIdType(TypeDecorator):
    """
    ObjectId类型数据
    入库：  id = ObjectId()
    出库：  字符串对象
    数据库操作： 可以当做ObjectId类型操作  XXX.where(id >= ObjectId(61442d972be5ef4b488a2a47))
    """

    impl = sqlalchemy.types.BINARY(12)
    cache_ok = True

    @property
    def python_type(self):
        """
        返回 Python 类型，用于 sqladmin 等工具识别字段类型
        ObjectIdType 在 Python 中表现为字符串（十六进制）
        """
        return str

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, ObjectId):
                return value.binary
            elif isinstance(value, str):
                return ObjectId(value).binary
            elif isinstance(value, bytes):
                return value
            else:
                return ObjectId(value).binary
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.hex()
        return None

    def __init__(self, length=None):  # 忽略length但是需要完成初始化占位
        super(ObjectIdType, self).__init__(self.impl)
