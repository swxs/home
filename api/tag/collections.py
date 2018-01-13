# -*- coding: utf-8 -*-

class Collections():
    def __init__(self, tag_list):
        self.tag_list = tag_list

    def to_front(self):
        return [tag.to_front() for tag in self.tag_list]
