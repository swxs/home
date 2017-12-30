# -*- coding: utf-8 -*-

# from envoy import run  #不知为何，用envoy.run，程序不能正确执行，会挂起
import os
from common.mqtt_utils import watch_msg
from common.log_utils import getLogger

log = getLogger('mqtt_listener')


def handler(msg):
    valid_msg = ['home_backend']
    if msg not in valid_msg:
        log.error('bad msg: %s' % msg)
        return
    log.debug(msg)
    cmd = '/data/www/%s' % msg
    os.system(cmd)


watch_msg('home', handler)
