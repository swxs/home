# -*- coding: utf-8 -*-
# @FILE    : models/user.py
# @AUTH    : code_creater

import datetime

import bson
from umongo import Document, fields

import core

# 本模块方法
from .. import consts


@core.mongodb_instance.register
class User(Document):
    username = fields.StringField(allow_none=True)
    description = fields.StringField(allow_none=True)
    avatar = fields.ObjectIdField(allow_none=True)
