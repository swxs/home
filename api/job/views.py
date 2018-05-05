# -*- coding: utf-8 -*-

from const import undefined, JOB_LIST_PER_PAGE
from common.Utils.pagenate import Page
from base import BaseHandler
import utils

class JobHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, job_id=None):
        if job_id:
            job = utils.get_job_by_job_id(job_id)
            return utils.to_front(job)
        else:
            page = self.get_argument('page', 1)
            job_list = utils.get_job_list()
            paged_job_list = Page(
                job_list,
                page=page,
                items_per_page=JOB_LIST_PER_PAGE)
            return [utils.to_front(job) for job in paged_job_list]

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
        job = utils.create_job(job_type=job_type, job_pay=job_pay, job_time=job_time, job_city=job_city, job_age=job_age, job_edu=job_edu, job_company_name=job_company_name, job_company_type=job_company_type, job_company_kind=job_company_kind, job_company_pn=job_company_pn, job_company_add=job_company_add, job_desc=job_desc, job_url=job_url)
        return utils.to_front(job)
    
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
        job = utils.get_job_by_job_id(job_id)
        utils.update_job(job, job_type=job_type, job_pay=job_pay, job_time=job_time, job_city=job_city, job_age=job_age, job_edu=job_edu, job_company_name=job_company_name, job_company_type=job_company_type, job_company_kind=job_company_kind, job_company_pn=job_company_pn, job_company_add=job_company_add, job_desc=job_desc, job_url=job_url)
        return utils.to_front(job)

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
        job = utils.get_job_by_job_id(job_id)
        utils.update_job(job, job_type=job_type, job_pay=job_pay, job_time=job_time, job_city=job_city, job_age=job_age, job_edu=job_edu, job_company_name=job_company_name, job_company_type=job_company_type, job_company_kind=job_company_kind, job_company_pn=job_company_pn, job_company_add=job_company_add, job_desc=job_desc, job_url=job_url)
        return utils.to_front(job)

    @BaseHandler.ajax_base
    def delete(self, job_id):
        job = utils.get_job_by_job_id(job_id)
        utils.delete_job(job)
        return None
