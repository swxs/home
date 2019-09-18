# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.ContainerGroupSwitch import *
from .Container import Container
from settings import instance
from document_utils import NAME_DICT

@instance.register
class ContainerGroupSwitch(Container):
    container_id_list = fields.ListField(fields.StringField(), allow_none=True)
    switch_list = fields.ListField(fields.StringField(), allow_none=True)

    class Meta:
        pass


NAME_DICT["ContainerGroupSwitch"] = ContainerGroupSwitch
