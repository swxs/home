# -*- coding: utf-8 -*-
# @File    : Helper_mongodb.py
# @AUTH    : swxs
# @Time    : 2018/7/24 10:23

import sys
import os
import pymongo
import datetime
import subprocess
from ..Metaclass.Singleton import Singleton


class MongodbDumperHelper(object, metaclass=Singleton):
    def __init__(self, address, port, dbname, username, password, authdb, output):
        self.MONGODB_ADDRESS = address
        self.MONGODB_PORT = port
        self.MONGODB_DBNAME = dbname
        self.MONGODB_USERNAME = username
        self.MONGODB_PASSWORD = password
        self.MONGODB_AUTHDB = authdb
        self.MONGODB_DUMP_DIR = output

    def dump(self, gzip=True):
        if sys.platform == 'win32':
            MONGODUMP_EXE = 'mongodump.exe'
        else:
            MONGODUMP_EXE = 'mongodump'

        args = list()
        if self.MONGODB_ADDRESS:
            args.append("--host {MONGODB_ADDRESS}".format(MONGODB_ADDRESS=self.MONGODB_ADDRESS))
        if self.MONGODB_PORT:
            args.append("--port {MONGODB_PORT}".format(MONGODB_PORT=self.MONGODB_PORT))
        if self.MONGODB_DBNAME:
            args.append("--db {MONGODB_DBNAME}".format(MONGODB_DBNAME=self.MONGODB_DBNAME))
        if self.MONGODB_USERNAME:
            args.append("-u {MONGODB_USERNAME}".format(MONGODB_USERNAME=self.MONGODB_USERNAME))
        if self.MONGODB_PASSWORD:
            args.append("-p {MONGODB_PASSWORD}".format(MONGODB_PASSWORD=self.MONGODB_PASSWORD))
        if self.MONGODB_AUTHDB:
            args.append("--authenticationDatabase {MONGODB_AUTHDB}".format(MONGODB_AUTHDB=self.MONGODB_AUTHDB))

        filename = os.path.join(self.MONGODB_DUMP_DIR, "{now:%Y%m%d%H%M%S}".format(now=datetime.datetime.now()))
        args.append("--out {filename}".format(filename=filename))

        if gzip:
            args.append("--gzip")

        cmd = '{MONGODUMP_EXE} {MONGODUMP_ARGS}'.format(MONGODUMP_EXE=MONGODUMP_EXE, MONGODUMP_ARGS=" ".join(args))
        os.system(cmd)

        return filename
