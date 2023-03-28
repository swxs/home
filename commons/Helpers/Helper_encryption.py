# -*- coding: utf-8 -*-

import hashlib


class Encryption:
    def __init__(self, salt=None):
        self.salt = salt

    def _get_md5(self, pwd):
        if self.salt:
            mix_str = pwd + self.salt
        else:
            mix_str = pwd
        data = hashlib.md5()
        data.update(mix_str.strip().encode('utf-8'))
        return data.hexdigest()

    def get_password(self, name=None):
        password = self._get_md5(name)
        for c in password:
            if c.isalpha():
                password_begin = password.index(c)
                password = password[password_begin].upper() + password[password_begin + 1 : password_begin + 12]
                break
        return password
