# -*- coding: utf-8 -*-

import datetime
from BaseDocument import BaseDocument
import models_fields
from common.Helpers.Helper_encryption import Encryption


class PasswordLock(BaseDocument):
    name = models_fields.StringField(unique=True)
    key = models_fields.StringField()
    website = models_fields.StringField()
    user_id = models_fields.StringField()
    created = models_fields.DateTimeField()
    updated = models_fields.DateTimeField()

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)

    @property
    def password(self):
        return Encryption.get_password(self.key)

    def to_front(self):
        data_dict = super(PasswordLock, self).to_front()
        data_dict["password"] = self.password
        return data_dict
