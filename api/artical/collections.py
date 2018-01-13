# -*- coding: utf-8 -*-

class Collections():
    def __init__(self, artical_list):
        self.artical_list = artical_list

    def to_front(self):
        return [artical.to_front() for artical in self.artical_list]
