# -*- coding: utf-8 -*-
'''
@author: xuyi
@created: 2016-12-14 17:53:34
@description:
@updated: 2016-12-14 17:53:34
'''
import datetime
import hashlib

import requests

is_delete = is_public = is_nessary = is_enable = yes_or_no = {
    'yes': 1,
    'no': 0
}

undefined = frozenset()

AJAX_SUCCESS = 0
AJAX_FAIL_NORMAL = 1
AJAX_FAIL_AUTH = 2
AJAX_FAIL_NOTLOGIN = 3
ERRCODE_LIST = [
    (AJAX_SUCCESS, u'成功'),
    (AJAX_FAIL_NORMAL, u'出错啦'),  # 前端可从response data的errmsg字段获取出错信息
    (AJAX_FAIL_AUTH, u'失败'),      # 前端需要重定向大登录页面
    (AJAX_FAIL_NOTLOGIN, u'失败'),  # 前端需要重定向到某个页面
]

if __name__ == "__main__":
    requests.post('http://localhost:8088/api/bi/datasources/create/', data={"name": "test"},
                  headers={"Content-Type": "application/x-www-form-urlencoded"})

ERRCODE_DICT = {
    AJAX_SUCCESS: u'成功',
    AJAX_FAIL_NORMAL: u'出错啦',  # 前端可从response data的errmsg字段获取出错信息
    AJAX_FAIL_AUTH: u'失败',      # 前端需要重定向大登录页面
    AJAX_FAIL_NOTLOGIN: u'失败',  # 前端需要重定向到某个页面
}

DEALER_PROJECT_PER_PAGE = 30
STRUCTURE_USER_LIST_PER_PAGE = 30
STRUCTURE_DEALER_LIST_PER_PAGE = 30
USER_LIST_PER_PAGE = 30
DEALER_LIST_PER_PAGE = 30
TEAM_LIST_PER_PAGE = 30
FRONT_END_MAIN_PER_PAGE = 5




if __name__ == "__main__":
    pass
