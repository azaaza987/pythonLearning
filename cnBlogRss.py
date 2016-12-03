#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliang
@license: Apache Licence
@contact: liangliangyy@gmail.com
@site: http://www.lylinux.org
@software: PyCharm
@file: cnBlogRss.py
@time: 2016/2/20 0:51
"""

from bs4 import BeautifulSoup
import urllib2
import datetime
import PyRSS2Gen
import re
import sys
import feedparser
from CommonHelper import *

from  gevent import monkey, Greenlet

monkey.patch_all()
import gevent
from gevent.pool import Pool

reload(sys)
sys.setdefaultencoding('utf-8')


class cnBlogRss():
    def __init__(self):
        self.__pool__ = Pool()
        self.myrss = PyRSS2Gen.RSS2(title='博客园',
                                    link='http://www.cnblogs.com/',
                                    description=str(datetime.date.today()),
                                    items=[]
                                    )
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        opener = urllib2.build_opener(httpHandler, httpsHandler)
        urllib2.install_opener(opener)
        self.baseurl = "http://feed.cnblogs.com/blog/sitehome/rss"

    def useragent(self, url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
                     "Referer": 'http://baidu.com/'}
        req = urllib2.Request(url, headers=i_headers)
        html = urllib2.urlopen(req, timeout=100).read()
        return html

    def download(self, entity):
        try:
            url = entity.link
            html = self.useragent(url)
            soup = BeautifulSoup(html)
            postbody = soup.find('div', id='cnblogs_post_body')

            rss = PyRSS2Gen.RSSItem(
                title=soup.title.string,
                link=url,
                description=str(postbody),
                pubDate=entity.published
            )
            self.myrss.items.append(rss)
        except:
            pass

    def getitems(self):
        feed = feedparser.parse(self.baseurl)
        for entity in feed.entries:
            print(entity.link)
            self.__pool__.spawn(self.download, entity)
        self.__pool__.join()

    def SaveRssFile(self, filename):
        finallxml = self.myrss.to_xml(encoding='utf-8')
        file = open(filename, 'w')
        file.writelines(finallxml)
        file.close()


if __name__ == '__main__':
    rss = cnBlogRss()
    rss.getitems()
    rss.SaveRssFile('/var/www/wordpress/cnblog.xml')
