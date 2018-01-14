# -*- coding: utf-8 -*-

import hashlib


class Encryption():
    @classmethod
    def get_md5(cls, pwd, salt=None):
        if salt:
            mix_str = pwd + salt
        else:
            mix_str = pwd
        data = hashlib.md5()
        data.update(mix_str.strip().encode('utf-8'))
        return data.hexdigest()

    @classmethod
    def get_password(cls, name=None, salt="b8862e668e5abbc99d8390347e7ac749"):
        password = cls.get_md5(name, salt)
        for c in password:
            if c.isalpha():
                password_begin = password.index(c)
                password = password[password_begin].upper() + password[password_begin + 1: password_begin + 12]
                break
        return password
