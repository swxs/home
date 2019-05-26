# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.ValueGroup import ValueGroup as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ValueGroup(BaseUtils):
    name = model.StringField()
    value = model.IntField()
    expression = model.StringField()

    def __init__(self, **kwargs):
        super(ValueGroup, self).__init__(**kwargs)

    @classmethod
    def get_value_group_by_value_group_id(cls, value_group_id):
        return cls.select(id=value_group_id)

