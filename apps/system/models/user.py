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
    created = fields.DateTimeField(
        requirement=False,
        default=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        requirement=False,
        default=datetime.datetime.now,
    )    
    username = fields.StringField(
        requirement=True,
    )
    description = fields.StringField(
        requirement=False,
    )
    avatar = fields.ObjectIdField(
        requirement=False,
    )
