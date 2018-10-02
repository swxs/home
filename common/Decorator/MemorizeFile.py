# -*- coding: utf-8 -*-
# @File    : MemorizeFile.py
# @AUTH    : swxs
# @Time    : 2018/9/26 20:11

OBJ_DICT = {}


def remove_key(key):
    if key in OBJ_DICT:
        del OBJ_DICT[key]


def remove_all_data_memorize():
    for key in OBJ_DICT:
        remove_key(key)


def remove_data_memorize_by_worktable_id(worktable_id):
    delete_keys_list = list()
    for key in OBJ_DICT:
        if key.split("_")[-1] == worktable_id:
            delete_keys_list.append(key)
    for key in delete_keys_list:
        remove_key(key)


def memorize_file(function):
    def helper(*args):
        key = "{0}_{1}".format(function.__name__, args[0])
        if key in OBJ_DICT:
            ret_obj = OBJ_DICT[key]
        else:
            ret_obj = function(*args)
            OBJ_DICT[key] = ret_obj
            print(OBJ_DICT.keys())
        return ret_obj

    return helper
