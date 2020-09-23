#!/bin/env python
# coding=utf8

"""
导入命令
先清空collections
db.user.drop()
db.brand.drop()
db.model.drop()
db.brand_tag_priority
gunzip *.gz
mongorestore.exe -d useragent .
"""

import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.curdir))
import datetime
import settings

script_path = os.path.dirname(os.path.abspath(__file__))

if sys.platform == 'win32':
    exe = 'd:\\mongodb3.2\\bin\\mongodump.exe'
else:
    exe = '/usr/local/mongodb3.2.6/bin/mongodump'
now = datetime.datetime.now()
fname = os.path.join(script_path, 'db_backup', now.strftime('%Y%m%d%H%M%S'))
cmd = '%s --db=%s --out=%s --gzip' % (exe, settings.MONGODB_DBNAME, fname)
print(cmd)
os.system(cmd)
