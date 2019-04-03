# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine_utils as model
from ..models.Column import Column as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Column(BaseUtils):
    col = model.StringField()
    realcol = model.StringField()
    readablecol = model.StringField()
    worktable_id = model.ObjectIdField()
    is_visible = model.BooleanField()
    is_unique = model.BooleanField()
    dtype = model.IntField()
    ttype = model.IntField()
    expression = model.StringField()
    value_group_id_list = model.StringField()

    def __init__(self, **kwargs):
        super(Column, self).__init__(**kwargs)
