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
@time: 2016/6/2 20:53
"""
from  gevent import monkey, Greenlet

monkey.patch_all()

import urllib2
import cookielib
from bs4 import BeautifulSoup
import gevent
from gevent.queue import Queue, Empty
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re

Base = declarative_base()


class Urls(Base):
    __tablename__ = 'urls'
    id = Column(String(100), primary_key=True)


class LaGouJob(Base):
    __tablename__ = 'lagoujob'
    id = Column(Integer(), primary_key=True)
    name = Column(String(300))
    maxsalary = Column(Integer())
    minsalary = Column(Integer())
    lagouurl = Column(String(300))
    position = Column(String(300))
    experience = Column(String(300))
    degree = Column(String(300))
    temptation = Column(String(300))
    area = Column(String(300))
    scale = Column(String(300))
    stage = Column(String(300))


class LaGouJobHelper():
    def __init__(self):
        self.__engine__ = create_engine('mysql://root:root@192.168.28.130/lagoujob?charset=utf8')
        Base.metadata.create_all(self.__engine__)

    def initdatabase(self):
        DBSession = sessionmaker(bind=self.__engine__)
        session = DBSession()
        session.execute("truncate table urls")
        session.commit()
        session.close()

    def Save(self, lagoujob):
        DBSession = sessionmaker(bind=self.__engine__)
        session = DBSession()
        session.add(lagoujob)
        session.commit()
        session.close()

    def CheckUrlExists(self, id):
        DBSession = sessionmaker(bind=self.__engine__)
        session = DBSession()
        objs = session.query(Urls).filter(Urls.id == id).all()
        session.close()
        return len(objs) > 0


class LaGouSpider():
    def __init__(self):
        self.baseurl = 'http://www.lagou.com'
        self.__tasks__ = Queue()
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.lagouHelper = LaGouJobHelper()
        self.lagouHelper.initdatabase()

    def useragent(self, url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
                     "Referer": 'http://baidu.com/'}
        # req = urllib2.Request(url, headers=i_headers)
        # html = urllib2.urlopen(req, timeout=100).read()
        # self.opener.addheaders(i_headers)

        return self.opener.open(url)

    def HandleJobPage(self, joburl):
        print 'HandleJobPage ' + joburl
        html = self.useragent(joburl)
        soup = BeautifulSoup(html, 'lxml')
        print soup.title.name

    def writelog(self, str):
        with open('lagoulog.txt', 'a') as file:
            file.writelines(str + '\n')
            file.close()

    def AnalyticsPage(self, link):
        html = self.useragent(link)
        soup = BeautifulSoup(html, 'lxml')
        for a in soup.find_all('a'):
            try:
                #a = str(a).decode('utf-8')
                link = a.get('href')
                pattern = re.compile(r'#\w*')
                link = pattern.sub('', link)

                if (link is not None) and (not self.lagouHelper.CheckUrlExists(link)):
                    url = Urls()
                    url.id = link
                    self.lagouHelper.Save(url)
                    self.__tasks__.put(link)
            except Exception, e:
                self.writelog(str(e) + "\n" + str(a))

    def HandlePageUrl(self):

        while not self.__tasks__.empty():
            link = self.__tasks__.get()
            # print link
            if link.find('http://www.lagou.com') >= 0:
                pattern = re.compile(r'http://www.lagou.com/jobs/\d+.html\w*')
                match = pattern.match(link)
                if match:
                    self.HandleJobPage(link)
                # if link.find('http://www.lagou.com/jobs') >= 0:
                #    self.HandleJobPage(link)
                self.AnalyticsPage(link)


"""
    def Start(self, url):
        html = self.useragent(url)
        soup = BeautifulSoup(html, 'lxml')
        for a in soup.find_all('a'):
            link = str(a.get('href'))
            print link

            if link.find('http://www.lagou.com') >= 0:
                pattern = re.compile(r'#\w*')
                link = pattern.sub('', link)
                if link.find('http://www.lagou.com/jobs') >= 0:
                    pattern = re.compile(r'http://www.lagou.com/jobs/\d+.html\w*')
                    match = pattern.match(link)
                    if match:
                        self.HandleJobPage(link)
                else:
                    self.Start(link)
"""

"""
url = Urls()
url.id = 'ff'
helper = LaGouJobHelper()

print (helper.CheckUrlExists(url.id))

"""
spider = LaGouSpider()

gevent.spawn(spider.AnalyticsPage, spider.baseurl).join()

gevent.joinall([
    gevent.spawn(spider.HandlePageUrl)
])

# spider.AnalyticsPage(spider.baseurl)
