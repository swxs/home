# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

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
