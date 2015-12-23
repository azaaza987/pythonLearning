#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liangliang'


"""blog : http://www.lylinux.org"""


import urllib2
import urllib
import  json
from bs4 import BeautifulSoup
import os
import eyed3
import requests
import  re
import sys
reload(sys)
sys.setdefaultencoding('utf8')





musicpath=r'F:\CloudMusic'

def writelog(str):
    file=open('nolrc.txt','a')
    file.write(str+'\n')
    file.close()

def writelrc(str):
    file=open('lrc.txt','a')
    file.write(str+'\n')
    file.close()

class BaiDuMusic():
    def __init__(self,name,artist):
        self.name=name
        self.artist=artist
    def __useragent(self,url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
    "Referer": 'http://baidu.com/'}
        req = urllib2.Request(url, headers=i_headers)
        html = urllib2.urlopen(req).read()
        return html
    def SearchBaidu(self):
        requrl='http://music.baidu.com/search?key='+self.name+'+'+self.artist
        rsp=self.__useragent(requrl)
        soup=BeautifulSoup(rsp,"lxml")
        div=soup.find("div", { "monkey" : "result-song" })
        if div is not None:
            ul=div.find('ul')
            for li in ul.findAll('li'):
                a =li.find('a')
                url='http://music.baidu.com/'+ a.get('href')
                return  url
    def GetLrc(self):
        url=self.SearchBaidu()
        rsp=self.__useragent(url)
        soup=BeautifulSoup(rsp,'lxml')
        div=soup.find("div", { "id" : "lyricCont" })
        print(div)
        lrcurl='http://music.baidu.com/'+div.get('data-lrclink')
        print(lrcurl)


class XiaMiLrc():
    def __init__(self,artist,title):
        self.artist=artist.replace(' ','%20')
        self.title=title.replace(' ','%20')
        self.havelrc=False


    def __useragent(self,url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
    "Referer": 'http://baidu.com/'}
        req = urllib2.Request(url, headers=i_headers)
        html = urllib2.urlopen(req).read()
        return html

    def SearchXiami(self):
        requrl='http://www.xiami.com/search/song-lyric?key='+self.artist+'+'+self.title
        #print(requrl)
        rsp=self.__useragent(requrl)
        soup=BeautifulSoup(rsp,'lxml')
        div=soup.find("div", { "class" : "all_LRC" })

        table=div.findAll("table", { "class" : "track_list" })

        if table is not None:
            self.havelrc=True
        for t in table:
            s=t.find("td", { "class" : "song_name" })
            a=t.find("td", { "class" : "song_artist" })

            if s and a:

                artist= re.sub('<(.*?)>','',str(a)).decode('utf-8').replace('\t','').replace('\n','').replace(' ','%20')

                name=re.sub('<(.*?)>','',str(s)).decode('utf-8').replace('\t','').replace('\n','').replace(' ','%20')
                #print artist,name
                try:
                    if self.artist== artist and self.title==name:
                        inputvalue=t.find(['input'])['value']
                        #print(inputvalue)
                        self.havelrc=True
                        lrcurl= self.__xiamilrc(inputvalue)
                        #print lrcurl
                        return self.__getlrcstr(lrcurl)
                except:
                    self.havelrc=False
                    return ''


    def __xiamilrc(self,value):

        requrl='http://www.xiami.com/song/playlist/id/'+value
        #print requrl
        rsp=self.__useragent(requrl)

        lrcid =  re.compile('<lyric_url>(.*?)</lyric_url>',re.S).findall(rsp)
        lrcurl= lrcid[0]
        return lrcurl
    def __getlrcstr(self,lrcurl):
        rsp=''
        rsp=self.__useragent(lrcurl)

        return rsp

class TtpodLrc():
    def __init__(self,artist,title):
        self.artist=artist.replace(' ','%20')
        self.title=title.replace(' ','%20')
        self.havelrc=False

    def __getlrc(self,neid):
        if not self.havelrc:
            return ''
        requrl="http://lp.music.ttpod.com/lrc/down?artist=" + self.artist + "&title=" + self.title + "&code=" +str( neid);
        req=urllib2.urlopen(requrl)
        rsp=req.read()
        jsonstr=json.loads(rsp)

        lrc=jsonstr['data']['lrc']
        return lrc


    def searchsong(self):
        requrl='http://so.ard.iyyin.com/search.do?q='+self.title+'+'+self.artist
        req=urllib2.urlopen(requrl)
        rsp=req.read()
        jsonstr=json.loads(rsp)
        neid=0
        neid=jsonstr['data'][0]['neid']
        self.havelrc=True
        return self.__getlrc(neid)



class ParseLrc():
    def __init__(self,path):
        self.path=path
        self.music=eyed3.load(path)
        self.artist=self.music.tag._getArtist()
        self.title=self.music.tag._getTitle()
        self.lrc=''
        self.dictTimeLrc={}
    def searchlrc(self):
        lrc=''
        try:
            print('xiami')
            xiami=XiaMiLrc(self.artist,self.title)
            lrc=xiami.SearchXiami()
            if lrc=='' or lrc==None or lrc is None:
                print('ttpod')
                ttpod=TtpodLrc(self.artist,self.title)
                lrc=ttpod.searchsong()
            self.lrc=lrc
            return lrc
        except:
            if self.artist and self.title:
                writelog(self.artist+'  '+self.title)
            return ''
    def __getstr(self,i):
        if i <10:
            return "0"+str(i)
        else:
            return str(i)
    def writelrc(self):
        music=eyed3.load(self.path)
        mylrcstr=''

        for i in range(00,05):
            for j in range(00,59):
                for k in range(00,99):
                    timespan=self.__getstr(i)+":"+self.__getstr(j)+"."+self.__getstr(k)
                    if self.dictTimeLrc.has_key(timespan):
                        lrc= self.dictTimeLrc[timespan]
                        mylrcstr+=lrc+'\n'
                        #print(lrc.decode('utf-8'))

        try:
            mylrcstr=mylrcstr.decode('utf8')
            mylrcstr=u''.join(mylrcstr)
            music.tag.lyrics.set(mylrcstr)
            music.tag.save()
        except:
            writelog(self.path)

    def replacetimespan(self,line,refind):
        for f in refind:
            line=line.replace(f,'')
        return line

    def parselrc(self):
        if self.lrc=='' or self.lrc is None:
            return
        pattern = re.compile(r'\[\d{2}:\d{2}\.\d{2}\]')
        for line in self.lrc.split('\n'):
            refind= pattern.findall(line)
            lrcres= self.replacetimespan(line,refind)
            for timespan in refind:
                timespan=timespan.replace('[','').replace(']','')
                self.dictTimeLrc[timespan]=lrcres


if __name__=='__main__':
    baidu=BaiDuMusic('阴天快乐','陈奕迅')
    baidu.GetLrc()
"""
    for root,dirs,files in os.walk(musicpath):
        for filepath in files:
            the_path = os.path.join(root,filepath)
            #the_path='E:\Music_back\The Beatles\Hey Jude\The Beatles - Hey Jude.mp3'
            if (the_path.find("mp3") != -1):
                print the_path
                parselrc=ParseLrc(the_path)
                parselrc.searchlrc()
                parselrc.parselrc()
                parselrc.writelrc()


    print 'the end!'"""