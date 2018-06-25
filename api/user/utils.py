# -*- coding: utf-8 -*-
# @File    : utils.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

from tornado.util import ObjectDict
from const import undefined
from BaseUtils import BaseUtils
import models_fields

class User(BaseUtils):
    username = models_fields.StringField()
    nickname = models_fields.StringField()
    password = models_fields.StringField()
    userinfo_id = models_fields.ModelIdField()
    created = models_fields.DatetimeField()
    updated = models_fields.DatetimeField()


    __attrs__ = ['username', 'nickname', 'password', 'userinfo_id']

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_front(self):
        #  TODO: 考虑是否可以简单的切换到 类似proto的数据格式，也可能在最后的返回层级定
        data = self.to_dict()
        del data["password"]
        return data
