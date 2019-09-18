# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.DatasourceMerged import DatasourceMerged as _
from .Datasource import Datasource
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceMerged(Datasource):
    datamerge_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceMerged, self).__init__(**kwargs)

    @async_property
    async def datamerge(self):
        from .Datamerge import Datamerge
        return await Datamerge.get_datamerge_by_datamerge_id(self.datamerge_id)

    @classmethod
    async def get_datasource_merged_by_datasource_merged_id(cls, datasource_merged_id):
        return await cls.select(id=datasource_merged_id)

