# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Artical import Artical as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Artical(BaseDAO):
    title = model.StringField()
    author = model.StringField()
    year = model.StringField()
    source = model.StringField()
    summary = model.StringField()
    content = model.StringField()
    ttype_id_list = model.StringField()
    tag_id_list = model.StringField()
    comment_id_list = model.StringField()

    def __init__(self, **kwargs):
        super(Artical, self).__init__(**kwargs)

    @classmethod
    def get_artical_by_artical_id(cls, artical_id):
        return cls.select(id=artical_id)

