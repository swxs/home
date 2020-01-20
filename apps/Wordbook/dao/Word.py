# -*- coding: utf-8 -*-
# @File    : Word.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from document_utils.consts import NAME_DICT
from ..models.Word import Word as WordModel
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/word")


class Word(BaseDAO):
    en = model.StringField()
    cn = model.StringField()
    number = model.IntField()
    last_time = model.DateTimeField()

    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)

    @classmethod
    async def get_word_by_word_id(cls, word_id):
        return await cls.select(id=word_id)


NAME_DICT[BaseDAO.__manager__]["Word"] = WordModel