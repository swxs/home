# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.Tag import Tag as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Tag(BaseUtils):
    name = model.StringField()
    color = model.StringField()

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
