# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model_creater

from ..dao.Publish import Publish as BasePublish


class Publish(BasePublish):
    def __init__(self, **kwargs):
        super(Publish, self).__init__(**kwargs)
