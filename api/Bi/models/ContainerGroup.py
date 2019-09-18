# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.ContainerGroup import *
from .Container import Container
from settings import instance
from document_utils import NAME_DICT

@instance.register
class ContainerGroup(Container):
    container_id_list = fields.ListField(fields.StringField(), allow_none=True)
    layout_list = fields.ListField(fields.StringField(), allow_none=True)

    class Meta:
        pass


NAME_DICT["ContainerGroup"] = ContainerGroup
