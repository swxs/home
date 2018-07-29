# -*- coding: utf-8 -*-

import datetime
from BaseDocument import BaseDocument
import models_fields


class Job(BaseDocument):
    job_type = models_fields.StringField()
    job_pay = models_fields.StringField()
    job_time = models_fields.StringField()
    job_city = models_fields.StringField()
    job_age = models_fields.StringField()
    job_edu = models_fields.StringField()
    job_company_name = models_fields.StringField()
    job_company_type = models_fields.StringField()
    job_company_kind = models_fields.StringField()
    job_company_pn = models_fields.StringField()
    job_company_add = models_fields.StringField()
    job_desc = models_fields.StringField()
    job_url = models_fields.StringField()

    def __init__(self, **kwargs):
        super(Job, self).__init__(**kwargs)
