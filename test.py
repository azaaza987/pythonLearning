#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: Apache Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: test.py
@time: 2016/6/2 22:40
"""

"""
from gevent.queue import Queue
import gevent
message_queue = Queue()

def receiver(n):
    while not message_queue.empty():
        message = message_queue.get()
        print('Received %s  message %s' % (n, message))
        gevent.sleep(2)

    print('Quitting time!')

def sender():
    for i in xrange(1,25):
        message_queue.put_nowait(i)

gevent.spawn(sender).join()

gevent.joinall([
    gevent.spawn(receiver, 'steve'),
    gevent.spawn(receiver, 'john'),
    gevent.spawn(receiver, 'nancy'),
    ])
"""


import eyed3
