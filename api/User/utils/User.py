# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

from ..dao.User import User as BaseUser


class User(BaseUser):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
