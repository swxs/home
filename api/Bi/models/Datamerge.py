# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Datamerge import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class Datamerge(BaseModelDocument):
    source_worktable_id = model.ObjectIdField()
    source_column_id_list = model.ListField()
    remote_worktable_id = model.ObjectIdField()
    remote_column_id_list = model.ListField()
    how = model.IntField(enums=DATAMERGE_HOW_LIST, default=DATAMERGE_HOW_LEFT)


NAME_DICT["Datamerge"] = Datamerge
