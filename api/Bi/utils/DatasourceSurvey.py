# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.DatasourceSurvey import DatasourceSurvey as _
from .Datasource import Datasource
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceSurvey(Datasource):
    survey_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceSurvey, self).__init__(**kwargs)

