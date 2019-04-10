# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.Datasource import Datasource as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Datasource(BaseUtils):
    name = model.StringField()

    def __init__(self, **kwargs):
        super(Datasource, self).__init__(**kwargs)

