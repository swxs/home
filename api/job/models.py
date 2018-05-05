# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
import api.job.enums as enums

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

    __attrs__ = ['job_type', 'job_pay', 'job_time', 'job_city', 'job_age', 'job_edu', 'job_company_name', 'job_company_type', 'job_company_kind', 'job_company_pn', 'job_company_add', 'job_desc', 'job_url']
    
    def __updateattr__(self, name, value):
        super(Job, self).__setattr__(name, value)

    def __unicode__(self):
        try:
            return self.oid
        except AttributeError:
            return self.oid

    @property
    def oid(self):
        return str(self.id)
