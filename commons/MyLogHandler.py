# -*- coding: utf-8 -*-
# @File    : MyLogHandler.py
# @AUTH    : swxs
# @Time    : 2018/9/28 10:42

import os
import time
from logging.handlers import TimedRotatingFileHandler
from stat import ST_CTIME, ST_MTIME

from concurrent_log_handler import ConcurrentRotatingFileHandler

from core import path


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, when="h", interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        filename = os.path.join(path.LOG_PATH, "log.out")
        super(MyTimedRotatingFileHandler, self).__init__(
            filename, when, interval, backupCount, encoding, delay, utc, atTime
        )

    def shouldRollover(self, record):
        t = int(time.time())
        if self.when.startswith("D") and time.localtime(t).tm_mday == time.localtime(self.rolloverAt).tm_mday:
            return 1
        if t >= self.rolloverAt:
            return 1

        return 0


class RFHandler(ConcurrentRotatingFileHandler):
    def __init__(
        self,
        mode="a",
        maxBytes=1024 * 1024,
        backupCount=20,
        encoding=None,
        debug=False,
        delay=None,
        use_gzip=False,
        owner=None,
        chmod=None,
        umask=None,
        newline=None,
        terminator="\n",
        unicode_error_policy="ignore",
    ):
        filename = os.path.join(path.LOG_PATH, "clog.out")
        super(RFHandler, self).__init__(
            filename,
            mode=mode,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            debug=debug,
            delay=delay,
            use_gzip=use_gzip,
            owner=owner,
            chmod=chmod,
            umask=umask,
            newline=newline,
            terminator=terminator,
            unicode_error_policy=unicode_error_policy,
        )
