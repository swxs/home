# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model_creater

from ..dao.Container import Container as BaseContainer


class Container(BaseContainer):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
