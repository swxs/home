# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine_utils as model
from ..models.Datafilter import Datafilter as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Datafilter(BaseUtils):
    name = model.StringField()
    column_id = model.ObjectIdField()
    worktable_id = model.ObjectIdField()
    dtype = model.IntField()
    custom_attr = model.DictField()

    def __init__(self, **kwargs):
        super(Datafilter, self).__init__(**kwargs)
