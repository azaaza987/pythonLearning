#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: Apache Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: geventtest.py
@time: 2016/5/28 21:43
"""

from  gevent import monkey, Greenlet
monkey.patch_all()

import gevent

import urllib2
from bs4 import BeautifulSoup

from gevent.pool import Pool
import requests
from gevent.queue import Queue

#tasks = Queue()

pool=Pool()

def download(url):
    lens = len(requests.get(url).content)
    print url + ' ' + str(lens)


def worker():
    pass
    #while not tasks.empty():
    #    task = tasks.get()
    #    download(task)
    #    gevent.sleep(0)


def boss():
    baseurl = 'http://www.lylinux.org/sitemap.html'
    html = urllib2.urlopen(baseurl).read()
    soup = BeautifulSoup(html, "lxml")
    for link in soup.findAll('a'):
        if 'lylinux' in link['href']:
            #gevent.sleep(0)
            thelink = link['href']
            #tasks.put(thelink)
            pool.spawn(download,thelink)

boss()
pool.join()


'''


import gevent
from gevent.queue import Queue, Empty

tasks = Queue(maxsize=3)

def worker(n):
    try:
        while True:
            task = tasks.get(timeout=1) # decrements queue size by 1
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0)
    except Empty:
        print('Quitting time!')

def boss():
    """
    Boss will wait to hand out work until a individual worker is
    free since the maxsize of the task queue is 3.
    """

    for i in xrange(1,10):
        tasks.put(i)
    print('Assigned all work in iteration 1')

    for i in xrange(10,20):
        tasks.put(i)
    print('Assigned all work in iteration 2')

gevent.joinall([
    gevent.spawn(boss),
    gevent.spawn(worker, 'steve'),
    gevent.spawn(worker, 'john'),
    gevent.spawn(worker, 'bob'),
])
'''