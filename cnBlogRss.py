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

reload(sys)
sys.setdefaultencoding('utf-8')


class cnBlogRss():
    def __init__(self):
        self.myrss = PyRSS2Gen.RSS2(title='博客园',
                                    link='http://www.cnblogs.com/',
                                    description=str(datetime.date.today()),
                                    items=[]
                                    )
        self.baseurl = "http://feed.cnblogs.com/blog/sitehome/rss"
    def useragent(self,url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
    "Referer": 'http://baidu.com/'}
        req = urllib2.Request(url, headers=i_headers)
        html = urllib2.urlopen(req).read()
        return html
    def getitems(self):
        feed = feedparser.parse(self.baseurl)
        for entity in feed.entries:
            print(entity.link)
            url = entity.link

            html=self.useragent(url)

            soup=BeautifulSoup(html)
            postbody=soup.find('div',id='cnblogs_post_body')

            #published
            rss=PyRSS2Gen.RSSItem(
                title=soup.title.string,
                link=url,
                description = str(postbody),
                pubDate = entity.published
            )
            self.myrss.items.append(rss)

    def SaveRssFile(self,filename):
        finallxml=self.myrss.to_xml(encoding='utf-8')
        file=open(filename,'w')
        file.writelines(finallxml)
        file.close()

if __name__ == '__main__':
    rss = cnBlogRss()
    rss.getitems()
    rss.SaveRssFile('/var/www/wordpress/cnblog.xml')
