# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model_creater

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

    @classmethod
    def get_tag_by_tag_id(cls, tag_id):
        return cls.select(id=tag_id)

