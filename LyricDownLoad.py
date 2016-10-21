#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: Apache Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: LyricDownLoad.py
@time: 2016/10/17 下午9:43
"""
from bs4 import BeautifulSoup
import requests
import eyed3
import re
import json
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

musicpath = r'/Users/liangliang/Music/music'


class Base():
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
        self.havelrc = False

    def useragent(self, url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
                     "Referer": 'http://baidu.com/'}
        rsp = requests.get(url, headers=i_headers)
        #print rsp.encoding
        rsp.encoding = rsp.apparent_encoding
        return rsp.text


class LyricTools():
    def __init__(self, lyric):
        self.lyric = lyric
        self.dictTimeLrc = {}

    def __getstr(self, i):

        if i < 10:
            return "0" + str(i)
        else:
            return str(i)

    def replacetimespan(self, line, refind):
        for f in refind:
            line = line.replace(f, '')
        return line

    def __parselrc(self):
        if self.lyric == '' or self.lyric is None:
            return

        pattern = re.compile(r'\[\d{2,3}:\d{2,3}\.\d{2,3}\]')
        for line in self.lyric.split('\n'):
            refind = pattern.findall(line)
            lrcres = self.replacetimespan(line, refind)
            for timespan in refind:
                timespan = timespan.replace('[', '').replace(']', '')
                # print timespan
                self.dictTimeLrc[timespan] = lrcres

    def parseLyric(self):
        self.__parselrc()
        mylrcstr = ''
        for i in range(00, 05):
            for j in range(00, 59):
                for k in range(00, 99):
                    timespan = self.__getstr(i) + ":" + self.__getstr(j) + "." + self.__getstr(k)
                    if self.dictTimeLrc.has_key(timespan):
                        lrc = self.dictTimeLrc[timespan]
                        # print lrc
                        mylrcstr += lrc + '\n'
        mylrcstr = mylrcstr.decode('utf8')
        mylrcstr = u''.join(mylrcstr)
        mylrcstr = unicode(mylrcstr)
        return mylrcstr


class BaiDuMusic(Base):
    def __init__(self, name, artiist):
        Base.__init__(self, name, artiist)
    def CheckLyric(self,url):
        html=self.useragent(url)
        soup=BeautifulSoup(html)
        titlespan=soup.find("span",{"class":"name"})
        authspan=soup.find("span",{"class":"author_list"})
        import chardet
        print  chardet.detect(str(titlespan.text))
        print str(titlespan.text)==self.name

        print str(authspan['title']).decode('gb18030').encode('utf-8')
    def Search(self):
        requrl = 'http://music.baidu.com/search?key=' + self.name + '+' + self.artist

        rsp = self.useragent(requrl)
        with open('text.txt','w') as file:
            file.writelines(rsp)
        soup = BeautifulSoup(rsp)
        div = soup.find("div", {"monkey": "result-song"})
        if div is not None:

            ul = div.find('ul')

            for li in ul.findAll('li'):
                a = li.find('a')
                url = 'http://music.baidu.com/' + a.get('href')

                titleem= li.find('em')
                authorli=li.find('span',{"class":"author_list"})
                if authorli and titleem:
                    authorem=authorli.find('em')
                    if authorem:
                        author=authorem.text
                        #print author
                        title=titleem.text
                        #print title
                        if author and  title:
                            if self.artist==author and self.name==title:
                                self.havelrc=True
                                return url
        return None

    def GetLyric(self, lyricUrl):
        if self.havelrc and lyricUrl != '':
            print lyricUrl
            rsp = self.useragent(lyricUrl)
            soup = BeautifulSoup(rsp, "lxml")
            div = soup.find("div", {"id": "lyricCont"})
            if div == None:
                return ''
            # print(div)
            # print lyricUrl
            lrcurl = div['data-lrclink']
            if lrcurl == None:
                return ''
            print(lrcurl)
            lrc = self.useragent(lrcurl)
            return lrc
        return None


class XiaMiLrc(Base):
    def __init__(self, name, artiist):
        Base.__init__(self, name, artiist)

    def GetLyric(self, lyricUrl):
        if self.havelrc and lyricUrl != '' and lyricUrl != None:
            print lyricUrl
            data = self.useragent(lyricUrl)
            return data

    def Search(self):
        requrl = 'http://www.xiami.com/search/song-lyric?key=' + self.artist + '+' + self.name
        print requrl
        rsp = self.useragent(requrl)

        soup = BeautifulSoup(rsp, 'lxml')
        div = soup.find("div", {"class": "all_LRC"})

        table = div.findAll("table", {"class": "track_list"})
        if table is not None:
            self.havelrc = True
            for t in table:
                s = t.find("td", {"class": "song_name"})
                a = t.find("td", {"class": "song_artist"})

                if s and a:
                    artist = re.sub('<(.*?)>', '', str(a)).decode('utf-8').replace('\t', '') \
                        .replace('\n', '').replace('MV%20', '').replace(' ', '')
                    name = re.sub('<(.*?)>', '', str(s)).decode('utf-8').replace('\t', '') \
                        .replace('\n', '').replace('MV%20', '').replace("MV", '').replace(' ', '')
                    # print artist,name
                    # print self.artist,self.name
                    try:
                        if self.artist == artist and self.name == name:
                            inputvalue = t.find(['input'])['value']
                            self.havelrc = True
                            requrl = 'http://www.xiami.com/song/playlist/id/' + inputvalue
                            # print requrl
                            rsp = self.useragent(requrl)

                            lrcid = re.compile('<lyric_url>(.*?)</lyric_url>', re.S).findall(rsp)
                            lrcurl = lrcid[0]
                            print lrcurl
                            return lrcurl
                            # print lrcurl
                            # return self.__getlrcstr(lrcurl)
                    except Exception, e:
                        print 'xiami error'
                        print e
                        self.havelrc = False
                        return ''


class TTpodLyric(Base):
    def __init__(self, name, artiist):
        Base.__init__(self, name, artiist)

    def GetLyric(self):
        url = 'http://lp.music.ttpod.com/lrc/down?artist=' + self.artist + '&title=' + self.name
        print url
        rsp = self.useragent(url)
        jsondata = json.loads(rsp)
        if str(jsondata['code']) == '1':
            self.havelrc = True
            return str(jsondata['data']['lrc'])


class MusicTools():
    def GetLyric(self, name, artiist):
        count = 0
        lyric = ''
        name = str(name).replace(' ', '')
        artiist = str(artiist).replace(' ', '')
        while count <= 3:
            # baidu
            #print name, artist
            count += 1
            if count == 1:
                print 'baidu'
                baidu = BaiDuMusic(name, artiist)
                url = baidu.Search()
                if not baidu.havelrc:
                    continue
                else:
                    lyric = baidu.GetLyric(url)
                    if lyric == '' or lyric == None:
                        continue
                    else:
                        break
            # xiami
            if count == 2:
                print 'xiami'
                xiami = XiaMiLrc(name, artiist)
                url = xiami.Search()
                if xiami.havelrc:
                    lyric = xiami.GetLyric(url)

                    if lyric == '' or lyric == None:
                        continue
                    else:
                        break
                else:
                    continue
            # ttpod
            if count == 3:
                print 'ttpod'
                ttpod = TTpodLyric(name, artiist)
                lyric = ttpod.GetLyric()
                if ttpod.havelrc:
                    break
                else:
                    continue
        if lyric != '':
            parser = LyricTools(lyric=lyric)
            data = parser.parseLyric()
            return data


if __name__ == '__main__':

    for root, dirs, files in os.walk(musicpath):
        for filepath in files:
            the_path = os.path.join(root, filepath)
            # the_path='E:\Music_back\The Beatles\Hey Jude\The Beatles - Hey Jude.mp3'
            if (the_path.find("mp3") != -1):
                music = eyed3.load(the_path)
                artist = music.tag._getArtist()
                title = music.tag._getTitle()
                tool = MusicTools()
                lyric = tool.GetLyric(title, artiist=artist)
                if lyric:
                    print "get lyric!!!!!!!!!"
                    lyric = lyric.decode('utf8')
                    lyric = u''.join(lyric)
                    lyric = unicode(lyric)
                    # mylrcstr=mylrcstr.encode('utf-8')

                    music.tag.lyrics.set(lyric)
                    # music.tag.lyrics[0].set(mylrcstr)
                    music.tag.save()
                #print lyric
    print 'the end!'
    """
    print 'the end!'
    name = "阴天快乐"
    artiist = "陈奕迅"
    # xiami = XiaMiLrc(name, artiist)
    # url = xiami.Search()
    # lyric = xiami.GetLyric(url)
    # print lyric
    # ttpod=TTpodLyric(name,artiist)
    # lyric=ttpod.GetLyric()

    baidu = BaiDuMusic(name, artiist)
    url = baidu.Search()
    lyric = baidu.GetLyric(url)


    # parser = LyricTools(lyric=lyric)
    # data = parser.parseLyric()
    # print data
    """
