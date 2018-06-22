# -*- coding: utf-8 -*-
# @File    : utils.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

from tornado.util import ObjectDict
from const import undefined
from BaseUtils import BaseUtils

class User(BaseUtils):
    __attrs__ = ['username', 'nickname', 'password', 'userinfo_id']

    # 校验参数是否可以使用select
    # __get_type__ = [
    #     ("id",),
    #     ("username",),
    # ]
    # 校验参数是否可以适用filter
    # __filter_type__ = [
    #     (),
    #     ("nickname",)
    # ]

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_front(self):
        #  TODO: 考虑是否可以简单的切换到 类似proto的数据格式，也可能在最后的返回层级定
        data = self.to_dict()
        del data["password"]
        return data


