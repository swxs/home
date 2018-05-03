# -*- coding: utf-8 -*-
# @File    : utils.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

from pandas import json
from tornado.util import ObjectDict
from const import undefined
from models_manager.manager_mongoenginee import Manager
from common.Utils import utils


class User():
    __attrs__ = ['username', 'nickname', 'password', 'userinfo_id']

    __get_one__ = [
        ("username",),
    ]

    __get_list__ = [
        (),
        ("nickname",)
    ]

    def __init__(self, **kwargs):
        self.name = kwargs.get('username', undefined)
        self.name = kwargs.get('nickname', undefined)
        self.password = kwargs.get('password', undefined)
        self.name = kwargs.get('userinfo_id', undefined)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password):
        self.__dict__["password"] = utils.get_password(password)

    def to_front(self):
        d = json.loads(self.to_dict())
        return ObjectDict(d)

    @classmethod
    def create(cls, **kwargs):
        return Manager.create('User', cls, **kwargs)

    @classmethod
    def select(cls, **kwargs):
        return Manager.select('User', cls, **kwargs)

    def udpate(self):
        return Manager.update('User', self)

    def delete(self):
        return Manager.delete('User', self)
