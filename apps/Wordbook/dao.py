# -*- coding: utf-8 -*-
# @FILE    : dao.py
# @AUTH    : model_creater

from dao import fields
from ..BaseDAO import BaseDAO
from . import consts
from common.Utils.log_utils import getLogger

log = getLogger("dao")


class Word(BaseDAO):
    en = fields.StringField()
    cn = fields.StringField()
    number = fields.IntField(default=0)
    last_time = fields.DateTimeField()

    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)

    @classmethod
    async def get_word_by_word_id(cls, word_id):
        return await cls.select(id=word_id)

