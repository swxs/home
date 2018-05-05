# -*- coding: utf-8 -*-

from tornado.web import url
import api.job.views as views

url_mapping = [
    url(r"/api/job/(\w+)/", views.JobHandler, name='select_job'),
    url(r"/api/job/", views.JobHandler, name='select_job_list'),
    url(r"/api/job/", views.JobHandler, name='create_job'),
    url(r"/api/job/(\w+)/", views.JobHandler, name='update_job'),
    url(r"/api/job/(\w+)/", views.JobHandler, name='modify_job'),
    url(r"/api/job/(\w+)/", views.JobHandler, name='delete_job'),
]
