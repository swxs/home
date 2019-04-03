# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.Container import Container as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Container(BaseUtils):
    name = model.StringField()
    show_name = model.BooleanField()

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
