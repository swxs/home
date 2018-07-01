# -*- coding: utf-8 -*-

import json
import datetime
import os

# import openpyxl
from bson import ObjectId
from tornado.util import ObjectDict
from mongoengine.errors import NotUniqueError
import settings
from const import undefined
from common.Decorator.mem_cache import memorize
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException
from common.Exceptions.ValidateException import ValidateException
from api.job.models import Job


def refresh(job):
    get_job_by_job_id(job.oid, refresh=1)


def create_job(**kwargs):
    job = Job()
    for attr in job.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            job.__updateattr__(attr, value)
    try:
        job.save()
    except NotUniqueError:
        raise ExistException("Job")
    return job


@memorize
def get_job_by_job_id(job_id):
    try:
        _id = ObjectId(job_id)
        return Job.objects.get(id=_id)
    except Job.DoesNotExist:
        raise NotExistException("Job")

def get_job_by_type_company_name(job_type, job_company_name):
    try:
        return Job.objects.get(job_type=job_type, job_company_name=job_company_name)
    except:
        return None

def get_job_list():
    return Job.objects.all()


def update_job(job, **kwargs):
    for attr in job.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            job.__updateattr__(attr, value)
    job.updated = datetime.datetime.now()
    try:
        job.save()
    except NotUniqueError:
        raise ExistException("Job")
    refresh(job)
    return job


def delete_job(job):
    job.delete()
    refresh(job)
    return None


def to_front(job):
    d = json.loads(job.to_json())
    d['id'] = job.oid
    d.pop('_id')
    return ObjectDict(d)


def to_excel():
    job_list = get_job_list()
    work_book = openpyxl.Workbook(write_only=True)
    sheet = work_book.create_sheet("BOSS直聘")
    datas = [
        "job_type",
        "job_pay",
        "job_time",
        "job_city",
        "job_age",
        "job_edu",
        "job_company_name",
        "job_company_type",
        "job_company_kind",
        "job_company_pn",
        "job_url",
    ]
    sheet.append(datas)
    for job in job_list:
        datas = [
            job.job_type,
            job.job_pay,
            job.job_time,
            job.job_city,
            job.job_age,
            job.job_edu,
            job.job_company_name,
            job.job_company_type,
            job.job_company_kind,
            job.job_company_pn,
            job.job_url,
        ]
        sheet.append(datas)
    work_book.save(os.path.join(settings.DATAFILE_PATH, "job.xlsx"))