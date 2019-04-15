# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.DatasourceMerged import DatasourceMerged as _
from .Datasource import Datasource
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceMerged(Datasource):
    datamerge_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceMerged, self).__init__(**kwargs)

    @property
    def datamerge(self):
        from .Datamerge import Datamerge
        return Datamerge.get_datamerge_by_datamerge_id(self.datamerge_id)

    @classmethod
    def get_datasource_merged_by_datasource_merged_id(cls, datasource_merged_id):
        return cls.select(id=datasource_merged_id)

