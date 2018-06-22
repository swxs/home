# -*- coding: utf-8 -*-

# from envoy import run  #不知为何，用envoy.run，程序不能正确执行，会挂起
import sys
from common.mqtt_utils import send_msg

topic = 'home'
try:
    msg = ' '.join(sys.argv[1:])
except IndexError:
    print('Usage: mqtt_cmd.py <message>')
    sys.exit(1)

if __name__ == '__main__':
    send_msg(topic, msg)
