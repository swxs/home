# -*- coding: utf-8 -*-
# @File    : Word.py
# @AUTH    : model_creater

from ..models.Word import Word as WordModel
from ..dao.Word import Word as BaseWord
from marshmallow import Schema, fields

WordSchema = WordModel.schema.as_marshmallow_schema()

word_schema = WordSchema()

class Word(BaseWord):
    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)
