# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model_creater

from ..dao.Tag import Tag as BaseTag


class Tag(BaseTag):
    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
