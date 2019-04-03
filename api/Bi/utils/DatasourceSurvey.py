# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.DatasourceSurvey import DatasourceSurvey as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceSurvey(BaseUtils):
    survey_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceSurvey, self).__init__(**kwargs)
