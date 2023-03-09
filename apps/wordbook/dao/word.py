# -*- coding: utf-8 -*-
# @File    : dao/word.py
# @AUTH    : code_creater


import logging

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.word import Word as WordModel

logger = logging.getLogger("main.apps.wordbook.dao.word")


class Word(BaseDocument):
    en = fields.StringField()
    cn = fields.StringField()
    number = fields.IntField()
    last_time = fields.DateTimeField()
    user_id = fields.ObjectIdField()

    class Meta:
        model = WordModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)
