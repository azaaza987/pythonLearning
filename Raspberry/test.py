#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: test.py
@time: 2017/5/13 上午3:31
"""

import os
import signal
import subprocess
import sys
import uuid

# 获取程序运行的本地目录，和用来存储接收结果的recv文件夹目录

BASEPATH = os.path.realpath(os.path.dirname(sys.argv[0]))
RECV = os.path.join(BASEPATH, 'recv')

# 如果接收目录不存在，就自动新建

print " *** Received files are put into: %s" % RECV
if not os.path.isdir(RECV):
    os.system('mkdir -p %s' % RECV)

# 下面的部分用来记录正在等待接收的文件。这个文件会以一个UUID.tmp的格式命名。
# 在接收成功后，就会被重命名为UUID。（UUID是一个特定格式的唯一字符串，不会重复）。
# 如果在接收过程中按下Ctrl+C，就会发送一个终止命令给程序，这样程序会退出，
# 并删除没有接收完整的那个文件。

working = False
fullname = False

def sigint_handler(signum, frame):
    global fullname, working
    print "\n"
    print " *** SIGINT detected. End the program."
    if working and fullname != False:
        print " *** Unfinished recording deleted."
        os.system('rm -f %s.tmp' % fullname)
    exit()
signal.signal(signal.SIGINT, sigint_handler)

# 使用一个死循环来不断运行netcat(nc)命令。

n = 1
while True:
    recname = str(uuid.uuid1())
    print " [%8d] Listening for file [%s]. Use Ctrl+C to stop this script." % (n, recname)
    fullname = os.path.join(RECV, recname)

    working = True # 标记接收开始
    # 使用 nc -lp 10401 命令接收数据，表明端口为10401。
    subprocess.call('nc -lp 10401 > %s.tmp' % fullname, shell=True)
    os.system('mv %s.tmp %s' % (fullname, fullname))
    working = False # 标记接收完毕

    n += 1