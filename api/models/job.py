# -*- coding: utf-8 -*-

import datetime
import mongoengine as models


class Job(models.Document):
    job_type = models.StringField()
    job_pay = models.StringField()
    job_time = models.StringField()
    job_city = models.StringField()
    job_age = models.StringField()
    job_edu = models.StringField()
    job_company_name = models.StringField()
    job_company_type = models.StringField()
    job_company_kind = models.StringField()
    job_company_pn = models.StringField()
    job_company_add = models.StringField()
    job_desc = models.StringField()
    job_url = models.StringField()
