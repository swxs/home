# -*- coding: utf-8 -*-
# @File    : MyLogHandler.py
# @AUTH    : swxs
# @Time    : 2018/9/28 10:42

import os
import time
from tornado import options
from stat import ST_MTIME, ST_CTIME
from logging.handlers import TimedRotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler
import settings


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        filename = os.path.join(settings.LOG_PATH, "log.out")

        super(MyTimedRotatingFileHandler, self).__init__(
            filename, when, interval, backupCount, encoding, delay, utc, atTime
        )

    def shouldRollover(self, record):
        t = int(time.time())
        if self.when.startswith('D') and time.localtime(t).tm_mday == time.localtime(self.rolloverAt).tm_mday:
            return 1
        if t >= self.rolloverAt:
            return 1

        return 0


class RFHandler(ConcurrentRotatingFileHandler):
    def __init__(
        self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None
    ):
        super(MyTimedRotatingFileHandler, self).__init__(
            options.LOG_PATH, when, interval, backupCount, encoding, delay, utc, atTime
        )
