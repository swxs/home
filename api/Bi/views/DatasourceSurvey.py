# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.DatasourceSurvey import DatasourceSurvey
from common.Utils.log_utils import getLogger

log = getLogger("views/DatasourceSurvey")


class DatasourceSurveyHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_survey_id=None):
        if datasource_survey_id:
            datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
            return DatasourceSurvey.to_front()
        else:
            datasource_survey_list = DatasourceSurvey.filter()
            return [datasource_survey.to_front() for datasource_survey in datasource_survey_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        datasource_survey = DatasourceSurvey.create(params)
        return datasource_survey.to_front()

    @BaseHandler.ajax_base()
    def put(self, datasource_survey_id):
        params = self.get_all_arguments()
        datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
        datasource_survey = datasource_survey.update(params)
        return datasource_survey.to_front()

    @BaseHandler.ajax_base()
    def patch(self, datasource_survey_id):
        params = self.get_all_arguments()
        datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
        datasource_survey = datasource_survey.update(params)
        return datasource_survey.to_front()

    @BaseHandler.ajax_base()
    def delete(self, datasource_survey_id):
        datasource_survey = DatasourceSurvey.select(id=datasource_survey_id)
        datasource_survey.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
