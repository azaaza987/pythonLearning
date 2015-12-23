#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liangliang'

from ebooklib import epub
from MyZhiHu import *
from SetLrc import *
import urllib2
import  json
from bs4 import BeautifulSoup


import  re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def getlrc(artist, title, neid):
    requrl="http://lp.music.ttpod.com/lrc/down?artist=" + artist + "&title=" + title + "&code=" +str( neid);
    req=urllib2.urlopen(requrl)
    rsp=req.read()
    jsonstr=json.loads(rsp)
    print(jsonstr['data']['lrc'])


def searchsong(songname,artiestname):
    requrl='http://so.ard.iyyin.com/search.do?q='+songname+'+'+artiestname
    req=urllib2.urlopen(requrl)
    rsp=req.read()

    #encodejson=json.dumps(rsp)
    jsonstr=json.loads(rsp)
    #print(jsonstr['data'])
    neid=jsonstr['data'][0]['neid']
    print(neid)
    getlrc(artiestname,songname,neid)

def useragent(url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
    "Referer": 'http://baidu.com/'}
        req = urllib2.Request(url, headers=i_headers)
        html = urllib2.urlopen(req).read()
        return html
def xiamisearch(songname,artiestname):
    requrl='http://www.xiami.com/search/song-lyric?key='+artiestname+'+'+songname
    rsp=useragent(requrl)
    soup=BeautifulSoup(rsp)
    div=soup.find("div", { "class" : "all_LRC" })
    table=div.find("table", { "class" : "track_list" })
    inputvalue=table.find(['input'])['value']
    print(inputvalue)
    xiamilrc(inputvalue)


def xiamilrc(value):
    requrl='http://www.xiami.com/song/playlist/id/'+value
    #print requrl
    rsp=useragent(requrl)
    #print rsp
    lrcid =  re.compile('<lyric_url>(.*?)</lyric_url>',re.S).findall(rsp)
    print lrcid[0]
if __name__=='__main__':

    #searchsong('我什么都没有','陈奕迅')
    xiamisearch('我什么都没有','陈奕迅')
    """
    lrc=SetLrc()
    lrc.ClearLrc()


    zhihu=MyZhiHu()
    zhihu.login()
    zhihu.GetCollection()
    """
    print('the end')
