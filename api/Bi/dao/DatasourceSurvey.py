# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model_creater

import datetime
import document_utils as model
from ..models.DatasourceSurvey import DatasourceSurvey as _
from .Datasource import Datasource
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceSurvey(Datasource):
    survey_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceSurvey, self).__init__(**kwargs)

    @classmethod
    def get_datasource_survey_by_datasource_survey_id(cls, datasource_survey_id):
        return cls.select(id=datasource_survey_id)

