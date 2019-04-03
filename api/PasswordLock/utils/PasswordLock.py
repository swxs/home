# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.PasswordLock import PasswordLock as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class PasswordLock(BaseUtils):
    name = model.StringField()
    key = model.StringField()
    website = model.StringField()
    user_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)
