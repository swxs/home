# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import re
import getpass
import time
import requests

current_user = getpass.getuser()


def get_pid(port):
    output = subprocess.getoutput('ps aux|grep "[p]ython main.py"')
    lines = output.split('\n')
    ps_dict = {}
    re_obj = re.compile(r'%s +(\d+).*main\.py (\d+)$' % current_user)
    for line in lines:
        result = re_obj.findall(line)
        if not result:
            continue
        pid, port1 = result[0]
        ps_dict[port1] = pid

    return ps_dict.get(str(port))


def usage():
    print('Usage: restart_port.py <port|all> <port_from> <process_number>')
    sys.exit(1)


def kill_port(port):
    pid = get_pid(port)
    if pid:
        cmd = 'kill -9 %s' % pid
        print('killing process ...')
        status, output = subprocess.getstatusoutput(cmd)
        # time.sleep(2)
        print('process %s for port %s is killed' % (pid, port))


def restart_port(port):
    pid = get_pid(port)
    if pid:
        cmd = 'kill -9 %s' % pid
        status, output = subprocess.getstatusoutput(cmd)
        time.sleep(1)
    cmd = 'nohup python main.py %s >> logs/p_%s.log &' % (port, port)
    # status,output = commands.getstatusoutput(cmd)
    os.system(cmd)


def check_port_is_health(port):
    need_check = True
    while need_check:
        time.sleep(1)
        try:
            response = requests.get('http://127.0.0.1:%s' % port)
            if response.status_code == 200:
                need_check = False
            else:
                need_check = True
                print('response.status_code=', response.status_code)
        except Exception as e:
            print('port=', port, str(e))
            need_check = True
        if need_check:
            print('port=', port)
            restart_port(port)


if __name__ == '__main__':
    try:
        port = sys.argv[1]
    except Exception:
        usage()

    if port == 'all':
        try:
            port_from = int(sys.argv[2])
        except Exception:
            usage()

        try:
            process_number = int(sys.argv[3])
        except Exception:
            usage()

        for port in range(port_from, port_from + process_number):
            restart_port(port)
            # check_port_is_health(port)
    elif port == 'kill':
        try:
            port_from = int(sys.argv[2])
        except Exception:
            usage()

        try:
            process_number = int(sys.argv[3])
        except Exception:
            usage()

        for port in range(port_from, port_from + process_number):
            kill_port(port)
    else:
        restart_port(port)
        check_port_is_health(port)
