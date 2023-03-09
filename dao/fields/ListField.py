# -*- coding: utf-8 -*-
# @File    : ListField.py
# @AUTH    : swxs
# @Time    : 2018/7/29 20:45

from bson import ObjectId

# 本模块方法
from .BaseField import BaseField


class ListField(BaseField):
    def __init__(self, **kwargs):
        if "strict" in kwargs:
            self.strict = kwargs.get("strict")
        super().__init__(**kwargs)

    def __set__(self, instance, value):
        if self.strict:
            if self.strict == ObjectId:
                new_value = list()
                for val in value:
                    if isinstance(val, ObjectId):
                        new_value.append(val)
                    else:
                        try:
                            new_value.append(ObjectId(val))
                        except Exception:
                            raise

            if not all(isinstance(val, self.strict) for val in value):
                raise Exception()

        super().__set__(instance, value)
