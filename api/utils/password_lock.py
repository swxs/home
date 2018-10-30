# -*- coding: utf-8 -*-

import datetime
import models_fields
from models_manager.BaseDocument import BaseDocument
from common.Helpers.Helper_encryption import Encryption


class PasswordLock(BaseDocument):
    name = models_fields.StringField()
    key = models_fields.StringField()
    website = models_fields.StringField()
    user_id = models_fields.StringField(max_length=24)
    created = models_fields.DateTimeField()
    updated = models_fields.DateTimeField(pre_update=datetime.datetime.now)

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)

    @property
    def user(self):
        from api.utils.user import User
        return User.select(id=self.user_id)

    @property
    def password(self):
        if self.key:
            return Encryption.get_password(name=self.key, salt=self.user.key)
        else:
            return None

    def to_front(self, *args, **kwargs):
        data_dict = super(PasswordLock, self).to_front()
        data_dict["password"] = self.password
        return data_dict
