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

import datetime
import PyRSS2Gen
import feedparser
import requests
from  gevent import monkey, Timeout
from gevent.pool import Pool

monkey.patch_all()

seconds = 360
timeout = Timeout(seconds)
timeout.start()


class cnBlogRss():
    def __init__(self):
        self.__pool__ = Pool()
        self.myrss = PyRSS2Gen.RSS2(title='博客园',
                                    link='http://www.cnblogs.com/',
                                    description=str(datetime.date.today()),
                                    items=[]
                                    )

        self.baseurl = "http://feed.cnblogs.com/blog/sitehome/rss"

    def useragent(self, url):
        i_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
            "Referer": 'http://baidu.com/'}
        rsp = requests.get(url, headers=i_headers)
        rsp.encoding = rsp.apparent_encoding
        return rsp.text

    def download(self, entity):
        try:
            url = entity.link

            html = self.useragent(url)
            soup = BeautifulSoup(html, 'lxml')
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
        try:
            self.__pool__.join()
        except:
            print('time out')

    def SaveRssFile(self, filename):
        print('start save')
        finallxml = self.myrss.to_xml(encoding='utf-8')
        file = open(filename, 'w')
        file.writelines(finallxml)
        file.close()
        print('save complate')


if __name__ == '__main__':
    rss = cnBlogRss()
    rss.getitems()
    rss.SaveRssFile('cnblog.xml')
