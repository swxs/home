# -*- coding: utf-8 -*-
# @File    : todo.py
# @AUTH    : swxs
# @Time    : 2018/8/15 11:28

STATUS_New = 1
STATUS_Doing = 2
STATUS_Waiting = 3
STATUS_Done = 4

STATUS_TYPES = [
    (STATUS_New, u'New'),
    (STATUS_Doing, u'Doing'),
    (STATUS_Waiting, u'Waiting'),
    (STATUS_Done, u'Done'),

]

SPECIES_Task = 1
SPECIES_Check = 2

SPECIES_TYPES = [
    (SPECIES_Task, u'Task'),
    (SPECIES_Check, u'Check'),

]

PRIORITY_Low = 1
PRIORITY_Normal = 2
PRIORITY_High = 3

PRIORITY_TYPES = [
    (PRIORITY_Low, u'Low'),
    (PRIORITY_Normal, u'Normal'),
    (PRIORITY_High, u'High'),
]
