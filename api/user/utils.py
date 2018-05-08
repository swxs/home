# -*- coding: utf-8 -*-
# @File    : utils.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

from pandas import json
from tornado.util import ObjectDict
from const import undefined
from BaseUtils import BaseUtils

class User(BaseUtils):
    __names__ = "User"

    __attrs__ = ['username', 'nickname', 'password', 'userinfo_id']

    __get_type__ = [
        ("id",),
        ("username",),
    ]

    __filter_type__ = [
        (),
        ("nickname",)
    ]

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_front(self):
        data = self.to_dict()
        del data["password"]
        return data


