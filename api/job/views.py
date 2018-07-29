# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
from api.job.utils import Job


class JobHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, job_id=None):
        if job_id:
            job = Job.select(id=job_id)
            return job.to_front()
        else:
            job_list = Job.filter()
            return [job.to_front() for job in job_list]

    @BaseHandler.ajax_base
    def post(self):
        job_type = self.get_argument('job_type', None)
        job_pay = self.get_argument('job_pay', None)
        job_time = self.get_argument('job_time', None)
        job_city = self.get_argument('job_city', None)
        job_age = self.get_argument('job_age', None)
        job_edu = self.get_argument('job_edu', None)
        job_company_name = self.get_argument('job_company_name', None)
        job_company_type = self.get_argument('job_company_type', None)
        job_company_kind = self.get_argument('job_company_kind', None)
        job_company_pn = self.get_argument('job_company_pn', None)
        job_company_add = self.get_argument('job_company_add', None)
        job_desc = self.get_argument('job_desc', None)
        job_url = self.get_argument('job_url', None)
        job = Job.create(
            job_type=job_type,
            job_pay=job_pay,
            job_time=job_time,
            job_city=job_city,
            job_age=job_age,
            job_edu=job_edu,
            job_company_name=job_company_name,
            job_company_type=job_company_type,
            job_company_kind=job_company_kind,
            job_company_pn=job_company_pn,
            job_company_add=job_company_add,
            job_desc=job_desc,
            job_url=job_url
        )
        return job.to_front()

    @BaseHandler.ajax_base
    def put(self, job_id):
        job_type = self.get_argument('job_type', None)
        job_pay = self.get_argument('job_pay', None)
        job_time = self.get_argument('job_time', None)
        job_city = self.get_argument('job_city', None)
        job_age = self.get_argument('job_age', None)
        job_edu = self.get_argument('job_edu', None)
        job_company_name = self.get_argument('job_company_name', None)
        job_company_type = self.get_argument('job_company_type', None)
        job_company_kind = self.get_argument('job_company_kind', None)
        job_company_pn = self.get_argument('job_company_pn', None)
        job_company_add = self.get_argument('job_company_add', None)
        job_desc = self.get_argument('job_desc', None)
        job_url = self.get_argument('job_url', None)
        job = Job.select(id=job_id)
        job = job.update(
            job_type=job_type,
            job_pay=job_pay,
            job_time=job_time,
            job_city=job_city,
            job_age=job_age,
            job_edu=job_edu,
            job_company_name=job_company_name,
            job_company_type=job_company_type,
            job_company_kind=job_company_kind,
            job_company_pn=job_company_pn,
            job_company_add=job_company_add,
            job_desc=job_desc,
            job_url=job_url
        )
        return job.to_front()

    @BaseHandler.ajax_base
    def patch(self, job_id):
        job_type = self.get_argument('job_type', undefined)
        job_pay = self.get_argument('job_pay', undefined)
        job_time = self.get_argument('job_time', undefined)
        job_city = self.get_argument('job_city', undefined)
        job_age = self.get_argument('job_age', undefined)
        job_edu = self.get_argument('job_edu', undefined)
        job_company_name = self.get_argument('job_company_name', undefined)
        job_company_type = self.get_argument('job_company_type', undefined)
        job_company_kind = self.get_argument('job_company_kind', undefined)
        job_company_pn = self.get_argument('job_company_pn', undefined)
        job_company_add = self.get_argument('job_company_add', undefined)
        job_desc = self.get_argument('job_desc', undefined)
        job_url = self.get_argument('job_url', undefined)
        job = Job.select(id=job_id)
        job = job.update(
            job_type=job_type,
            job_pay=job_pay,
            job_time=job_time,
            job_city=job_city,
            job_age=job_age,
            job_edu=job_edu,
            job_company_name=job_company_name,
            job_company_type=job_company_type,
            job_company_kind=job_company_kind,
            job_company_pn=job_company_pn,
            job_company_add=job_company_add,
            job_desc=job_desc,
            job_url=job_url
        )
        return job.to_front()

    @BaseHandler.ajax_base
    def delete(self, job_id):
        job = Job.select(id=job_id)
        job.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
