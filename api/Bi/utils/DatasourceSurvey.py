# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model_creater

from ..dao.DatasourceSurvey import DatasourceSurvey as BaseDatasourceSurvey


class DatasourceSurvey(BaseDatasourceSurvey):
    def __init__(self, **kwargs):
        super(DatasourceSurvey, self).__init__(**kwargs)
