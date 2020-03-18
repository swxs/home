# -*- coding: utf-8 -*-
# @File    : Organization.py
# @AUTH    : model_creater

from ..models.Organization import Organization as OrganizationModel
from ..dao.Organization import Organization as BaseOrganization
from marshmallow import Schema, fields

OrganizationSchema = OrganizationModel.schema.as_marshmallow_schema()

organization_schema = OrganizationSchema()

class Organization(BaseOrganization):
    def __init__(self, **kwargs):
        super(Organization, self).__init__(**kwargs)
