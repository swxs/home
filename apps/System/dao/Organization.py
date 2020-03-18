# -*- coding: utf-8 -*-
# @File    : Organization.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from document_utils.consts import NAME_DICT
from ..models.Organization import Organization as OrganizationModel
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/organization")


class Organization(BaseDAO):
    code = model.StringField()
    name = model.StringField()
    email = model.StringField()
    phone = model.StringField()
    status = model.IntField()

    def __init__(self, **kwargs):
        super(Organization, self).__init__(**kwargs)

    @classmethod
    async def get_organization_by_organization_id(cls, organization_id):
        return await cls.select(id=organization_id)


NAME_DICT[BaseDAO.__manager__]["Organization"] = OrganizationModel