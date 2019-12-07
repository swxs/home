# -*- coding: utf-8 -*-
# @File    : Word.py
# @AUTH    : model_creater

from ..dao.Word import Word as BaseWord


class Word(BaseWord):
    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)
