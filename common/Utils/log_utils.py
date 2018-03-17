# encoding=utf8

import log4py
import settings


def getLogger(name=''):
    log = log4py.Logger().get_instance(name)
    return log


def getRedisLogger(name=''):
    '''将log推入redis队列等待邮件发送'''
    log = log4py.Logger().get_instance(name)
    log.add_target(log4py.TARGET_REDIS_LIST,
                   settings.REDIS_HOST,
                   settings.REDIS_PORT,
                   settings.REDIS_DB,
                   settings.REDIS_PASSWORD,
                   settings.REDIS_LOG_MAIL_LIST_NAME)
    return log
