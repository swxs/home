# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.DatasourceSurvey import DatasourceSurvey

log = getLogger("views/DatasourceSurvey")


class DatasourceSurveyHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_survey_id=None):
        if datasource_survey_id:
            datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
            return datasource_survey.to_front()
        else:
            datasource_survey_list = DatasourceSurvey.filter()
            return [datasource_survey.to_front() for datasource_survey in datasource_survey_list]

    @BaseHandler.ajax_base()
    def post(self, datasource_survey_id=None):
        if datasource_survey_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['survey_id'] = self.get_argument('survey_id', undefined)
            datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
            datasource_survey = datasource_survey.copy(**params)
            return datasource_survey.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['survey_id'] = self.get_argument('survey_id', None)
            datasource_survey = DatasourceSurvey.create(**params)
            return datasource_survey.id

    @BaseHandler.ajax_base()
    def put(self, datasource_survey_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['survey_id'] = self.get_argument('survey_id', None)
        datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
        datasource_survey = datasource_survey.update(**params)
        return datasource_survey.id

    @BaseHandler.ajax_base()
    def patch(self, datasource_survey_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['survey_id'] = self.get_argument('survey_id', undefined)
        datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
        datasource_survey = datasource_survey.update(**params)
        return datasource_survey.id

    @BaseHandler.ajax_base()
    def delete(self, datasource_survey_id=None):
        datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
        datasource_survey.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
