# -*- coding: utf-8 -*-

class Collections():
    def __init__(self, password_lock_list):
        self.password_lock_list = password_lock_list

    def to_front(self):
        return [password_lock.to_front() for password_lock in self.password_lock_list]
