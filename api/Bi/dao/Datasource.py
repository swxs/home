# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Datasource import Datasource as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Datasource(BaseDAO):
    name = model.StringField()

    def __init__(self, **kwargs):
        super(Datasource, self).__init__(**kwargs)

    @classmethod
    def get_datasource_by_datasource_id(cls, datasource_id):
        return cls.select(id=datasource_id)

