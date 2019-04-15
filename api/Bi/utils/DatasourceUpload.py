# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.DatasourceUpload import DatasourceUpload as _
from .Datasource import Datasource
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceUpload(Datasource):
    filename = model.StringField()

    def __init__(self, **kwargs):
        super(DatasourceUpload, self).__init__(**kwargs)

    @classmethod
    def get_datasource_upload_by_datasource_upload_id(cls, datasource_upload_id):
        return cls.select(id=datasource_upload_id)

