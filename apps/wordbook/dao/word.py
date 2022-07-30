# -*- coding: utf-8 -*-
# @File    : dao/word.py
# @AUTH    : code_creater

import logging
import datetime

import bson

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.word import Word as WordModel

logger = logging.getLogger("main.apps.wordbook.dao.word")


class Word(BaseDocument):
    en = fields.StringField(
        allow_none=True,
    )
    cn = fields.StringField(
        allow_none=True,
    )
    number = fields.IntField(
        allow_none=True,
        default=0,
    )
    last_time = fields.DateTimeField(
        allow_none=True,
    )
    user_id = fields.ObjectIdField(
        allow_none=True,
    )

    class Meta:
        model = WordModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)
