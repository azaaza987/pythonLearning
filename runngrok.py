#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: runngrok.py
@time: 2017/5/16 下午10:42
"""

import os
import datetime
from common.PushbulletHelper import PushbullectHelper


def writelog(s):
    with open('runngrok.log', 'a') as file:
        s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\t" + s + "\n"
        print s
        file.writelines(s)


def server_is_run():
    cmd = 'nc -w 1 lylinux.org 4443 && echo 1 || echo 0'
    result = os.popen(cmd).readline().replace('\n', '').replace(' ', '')
    print result
    writelog("server not run" if result != "1" else "server running")
    return result == '1'


def loc_is_run():
    cmd = "pgrep ngrok"
    result = os.popen(cmd).readlines()
    if len(result) == 0:
        writelog("local not run")
        return ''
    else:
        writelog("local running ")
        return result[0].replace('\n', '').replace(' ', '')


server = server_is_run()
loc = loc_is_run()
if not server and loc != '':
    writelog('kill local')
    print 'kill local'
    pb = PushbullectHelper()
    pb.sendnote('ngrok', 'kill ngrok local ')
    os.system('kill -9 ' + loc)
elif server and loc == '':
    writelog("run loc")
    pb = PushbullectHelper()
    pb.sendnote('ngrok', 'local ngrok start running!!!')
    os.system(
        'nohup /home/pi/ngrok/linux_arm/ngrok -log=stdout -config=/home/pi/ngrok/ngrok.yml start-all > /home/pi/ngrok.log & ')
else:
    print 'ok'
