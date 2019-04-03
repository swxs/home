# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

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
