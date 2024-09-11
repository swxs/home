# -*- coding: utf-8 -*-
# @File    : dao/file_info.py
# @AUTH    : code_creater

import logging
import datetime

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.file_info import FileInfo as FileInfoModel

logger = logging.getLogger("main.apps.upload.dao.file_info")


class FileInfo(BaseDocument):
    id = fields.PrimaryField()
    created = fields.DateTimeField(
        default_create=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        default_create=datetime.datetime.now,
        default_update=datetime.datetime.now,
    )
    file_id = fields.StringField()
    file_name = fields.StringField()
    file_size = fields.IntField(
        default_create=0,
    )
    ext = fields.StringField()
    policy = fields.IntField(
        enums=consts.FILE_INFO_POLICY_LIST,
    )

    class Meta:
        model = FileInfoModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(FileInfo, self).__init__(**kwargs)
