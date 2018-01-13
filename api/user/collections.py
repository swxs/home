# -*- coding: utf-8 -*-

class Collections():
    def __init__(self, user_list):
        self.user_list = user_list

    def to_front(self):
        return [user.to_front() for user in self.user_list]
