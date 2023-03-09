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
        required=True,
        unique=False,
        allow_none=False,
    )
    updated = fields.DateTimeField(
        required=True,
        unique=False,
        allow_none=False,
    )
    username = fields.StringField(
        required=True,
        unique=True,
        allow_none=False,
    )
    description = fields.StringField(
        required=False,
        unique=False,
        allow_none=True,
    )
    avatar = fields.ObjectIdField(
        required=False,
        unique=False,
        allow_none=True,
    )
