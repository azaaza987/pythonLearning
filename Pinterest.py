#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: Apache Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: Pinterest.py
@time: 2016/5/28 21:37
"""

from  gevent import monkey, Greenlet

monkey.patch_all()
import gevent
import urllib2
import urllib
import json
from gevent.pool import Pool


class Pinterest():
    def __init__(self, token):
        self.__token__ = token
        self.__pool__ = Pool()

    def __downimg__(self, imgurl):
        content = urllib2.urlopen(imgurl).read()
        with open(u'D:\myimg' + '/' + imgurl[-31:], 'wb') as code:
            code.write(content)

    def __AddImgUrl__(self, url):
        self.__pool__.spawn(self.__downimg__, url)

    def SetBoardsInfo(self, boardsid):
        url = 'https://api.pinterest.com/v1/boards/' + boardsid + '/pins/?access_token=' + self.__token__ + \
              '&fields=id%2Clink%2Cnote%2Curl%2Cimage'
        jsoncontent = urllib2.urlopen(url).read()
        jsonobject = json.loads(jsoncontent, encoding='utf-8')
        data = jsonobject['data']

        for item in data:
            image = item['image']['original']['url']
            self.__AddImgUrl__(image)

    def SetBoardsInfoByIds(self, ids):
        for id in ids:
            self.SetBoardsInfo(id)
            #self.__pool__.spawn(self.SetBoardsInfo, id)

    def GetFollowingBoards(self):
        url = 'https://api.pinterest.com/v1/me/following/boards/?access_token=' + self.__token__ + '&fields=id%2Cname%2Curl'
        jsoncontent = urllib2.urlopen(url).read()
        jsonobject = json.loads(jsoncontent, encoding='utf-8')
        data = jsonobject['data']
        ids = []
        for item in data:
            id = item['id']
            ids.append(id)
            # self.__pool__.spawn(self.SetBoardsInfo, id)
        return ids

    def DownLoad(self):
        self.__pool__.join()


if __name__ == '__main__':
    p = Pinterest('AdXJzurbtchs4yuf7sM6cNoOGdMBFFK9FxWDBIFDIIGc_-BF3QAAAAA')
    ids = p.GetFollowingBoards()
    print ids

    p.SetBoardsInfoByIds(ids)
    p.DownLoad()
