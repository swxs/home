# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.Ttype import Ttype as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Ttype(BaseUtils):
    name = model.StringField()

    def __init__(self, **kwargs):
        super(Ttype, self).__init__(**kwargs)

    @classmethod
    def get_ttype_by_ttype_id(cls, ttype_id):
        return cls.select(id=ttype_id)

