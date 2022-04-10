# -*- coding: utf-8 -*-
# @FILE    : model_consts.py
# @AUTH    : model_creater


from enum import Enum

TODO_STATUS_NEW = 1
TODO_STATUS_DOING = 2
TODO_STATUS_WAITING = 3
TODO_STATUS_DONE = 4

TODO_STATUS_LIST = [
    (TODO_STATUS_NEW, '新建'),
    (TODO_STATUS_DOING, '进行中'),
    (TODO_STATUS_WAITING, '暂停中'),
    (TODO_STATUS_DONE, '完成'),
]

TODO_PRIORITY_LOW = 1
TODO_PRIORITY_NORMAL = 2
TODO_PRIORITY_HIGH = 3

TODO_PRIORITY_LIST = [
    (TODO_PRIORITY_LOW, '低'),
    (TODO_PRIORITY_NORMAL, '中'),
    (TODO_PRIORITY_HIGH, '高'),
]
