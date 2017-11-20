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
import sys
import re
import json
import os
from abc import ABCMeta, abstractmethod, abstractproperty
import argparse
from NeteaseCloudMusicApi.api import *

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='音乐路径')
parser.add_argument('--savepath', help='保存歌词文件的路径,默认将歌词写入音乐文件中。')
args = parser.parse_args()
musicpath = args.path
savepath = args.savepath

#musicpath = r'/Users/liangliang/Music/网易云音乐'


class LyricTools():
    def __init__(self, lyric):
        self.lyric = lyric

    def __getstr(self, span):

        s = list(map(lambda i: str(i) if i >= 10 else '0' + str(i), span))
        data = '{i}:{j}.{k}'.format(i=s[0], j=s[1], k=s[2])
        return data

    def replacetimespan(self, line, refind):
        for f in refind:
            line = line.replace(f, '')
        return line

    def parse_lrc_to_dict(self):
        if self.lyric == '' or self.lyric is None:
            return
        timelrc = dict()
        pattern = re.compile(r'\[\d{1,3}:\d{1,3}\.\d{1,3}\]')
        for line in self.lyric.split('\n'):
            refind = pattern.findall(line)
            lrcres = self.replacetimespan(line, refind)
            for timespan in refind:
                timespan = timespan.replace('[', '').replace(']', '')
                timelrc[timespan] = lrcres
        return timelrc

    def parse_lyric_dict(self, dictTimeLrc):

        mylrcstr = ''
        for i in range(0, 5):
            for j in range(00, 59):
                for k in range(00, 99):
                    timespan = self.__getstr((i, j, k))
                    if timespan in dictTimeLrc:
                        lrc = dictTimeLrc[timespan]

                        mylrcstr += lrc + '\n'

        return mylrcstr


class Base():
    SearchType = None

    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
        self.lrcdict = dict()
        self.lrcurl = ''
        self.lrc = ''

    @property
    def have_lrc_url(self):
        return self.lrcurl and self.lrcurl != ''

    def check_music_correct(self, checkname, checkartist):
        def clean(s):
            result = s.replace(' ', '').replace('-', '').upper()
            return result

        checkname = clean(checkname)
        checkartist = clean(checkartist)
        tempname = clean(self.name)
        tempartist = clean(self.artist)
        return checkname == tempname and checkartist == tempartist

    @property
    def have_lrc_data(self):
        return self.have_lrc_url and self.lrc

    def useragent(self, url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
                     "Referer": 'http://baidu.com/'}
        rsp = requests.get(url, headers=i_headers)
        rsp.encoding = rsp.apparent_encoding
        return rsp.text

    @abstractmethod
    def search_music(self):
        print("{type} start search {music}-{artist}".format(music=self.name, artist=self.artist, type=self.SearchType))

    @abstractmethod
    def getlrc_content(self):
        pass

    def parselrc(self, lrc_content):
        if lrc_content:
            print("{type} start parse lrc  {music}-{artist}".format(music=self.name, artist=self.artist,
                                                                    type=self.SearchType))
            parser = LyricTools(lyric=lrc_content)
            lrcdict = parser.parse_lrc_to_dict()
            self.lrcdict = lrcdict
            self.lrc = parser.parse_lyric_dict(lrcdict)
            return self.lrc


class NeteaseCloudMusic(Base):
    SearchType = 'netease'

    def __init__(self, name, artist):
        super(NeteaseCloudMusic, self).__init__(name, artist)
        self.netease = NetEase()

    def search_music(self):
        super(NeteaseCloudMusic, self).search_music()

        result = self.netease.search_by_artists_name(self.name, self.artist)
        if result:
            id = result['id']
            self.lrcurl = id
            return result
        return None

    def getlrc_content(self):
        musicid = self.lrcurl
        if musicid:
            lyric = self.netease.song_lyric(musicid)
            self.lrc = lyric
            return lyric
        return None


class BaiDuMusic(Base):
    SearchType = 'baidu'

    def __init__(self, name, artist):
        super(BaiDuMusic, self).__init__(name, artist)

    def search_music(self):
        super(BaiDuMusic, self).search_music()
        requrl = 'http://music.baidu.com/search?key=' + self.name + '+' + self.artist
        rsp = self.useragent(requrl)
        soup = BeautifulSoup(rsp, 'lxml')
        div = soup.find("div", {"monkey": "result-song"})
        if div:
            ul = div.find('ul')
            for li in ul.findAll('li'):
                a = li.find('a')
                url = 'http://music.baidu.com/' + a.get('href')
                titleem = li.find('em')
                authorli = li.find('span', {"class": "author_list"})
                if authorli and titleem:
                    authorem = authorli.find('em')
                    if authorem:
                        author = authorem.text

                        title = titleem.text
                        if author and title:
                            if self.check_music_correct(title, artist):
                                self.lrcurl = url
                                return url
        return None

    def getlrc_content(self):
        if self.have_lrc_url:
            super(BaiDuMusic, self).getlrc_content()
            rsp = self.useragent(self.lrcurl)
            soup = BeautifulSoup(rsp, "lxml")
            div = soup.find("div", {"id": "lyricCont"})
            if div == None:
                return ''
            lrcurl = div['data-lrclink']
            if lrcurl == None:
                return ''
            lrc = self.useragent(lrcurl)
            self.lrc = lrc
            return lrc
        return None


class XiaMiLrc(Base):
    SearchType = 'xiami'

    def __init__(self, name, artist):
        super(XiaMiLrc, self).__init__(name, artist)

    def getlrc_content(self):
        if self.have_lrc_url:
            super(XiaMiLrc, self).getlrc_content()
            data = self.useragent(self.lrcurl)
            self.lrc = data
            return data

    def search_music(self):
        super(XiaMiLrc, self).search_music()
        requrl = 'http://www.xiami.com/search/song-lyric?key=' + self.artist + '+' + self.name

        rsp = self.useragent(requrl)

        soup = BeautifulSoup(rsp, 'lxml')
        div = soup.find("div", {"class": "all_LRC"})

        table = div.findAll("table", {"class": "track_list"})
        if table is not None:
            for t in table:
                s = t.find("td", {"class": "song_name"})
                a = t.find("td", {"class": "song_artist"})

                if s and a:
                    artist = re.sub('<(.*?)>', '', str(a)).replace('\t', '') \
                        .replace('\n', '').replace('MV%20', '').replace(' ', '')
                    name = re.sub('<(.*?)>', '', str(s)).replace('\t', '') \
                        .replace('\n', '').replace('MV%20', '').replace("MV", '').replace(' ', '')
                    try:

                        if self.check_music_correct(name, artist):
                            inputvalue = t.find(['input'])['value']
                            self.havelrc = True
                            requrl = 'http://www.xiami.com/song/playlist/id/' + inputvalue
                            rsp = self.useragent(requrl)

                            lrcid = re.compile('<lyric_url>(.*?)</lyric_url>', re.S).findall(rsp)
                            lrcurl = lrcid[0]
                            self.lrcurl = lrcurl
                            return lrcurl
                    except Exception as e:
                        print('xiami error')
                        print(e)
                        return ''


class TTpodLyric(Base):
    SearchType = 'ttpod'

    def __init__(self, name, artist):
        name = str(name).replace(' ', '')
        artist = str(artist).replace(' ', '')
        super(TTpodLyric, self).__init__(name, artist)

    def search_music(self):
        super(TTpodLyric, self).search_music()
        url = 'http://lp.music.ttpod.com/lrc/down?artist=' + self.artist + '&title=' + self.name
        self.lrcurl = url
        return url

    def getlrc_content(self):
        if self.have_lrc_url:
            super(TTpodLyric, self).getlrc_content()
            rsp = self.useragent(self.lrcurl)
            jsondata = json.loads(rsp)
            if str(jsondata['code']) == '1':
                self.lrc = str(jsondata['data']['lrc'])
                return self.lrc


class MusicTools():
    def __get_music_apps(self, name, artist):
        applications = Base.__subclasses__()
        return list(map(lambda x: x(name, artist), applications))

    def GetLyric(self, name, artist):
        apps = self.__get_music_apps(name, artist)
        for app in apps:
            app.search_music()
            app.getlrc_content()
            if app.have_lrc_data:
                print('{apptype} get lrc...'.format(apptype=app.SearchType))
                lrc = app.parselrc(app.lrc)
                return lrc


if __name__ == '__main__':
    if savepath:
        if not os.path.exists(path=savepath):
            print('歌词保存路径不存在')
            sys.exit(0)
    if not musicpath:
        print('音乐文件不存在')
        sys.exit(0)
    for root, dirs, files in os.walk(musicpath):
        for filepath in files:
            the_path = os.path.join(root, filepath)
            if (the_path.find("mp3") != -1):
                music = eyed3.load(the_path)
                artist = music.tag._getArtist()
                title = music.tag._getTitle()
                tool = MusicTools()
                lyric = tool.GetLyric(title, artist)
                if lyric:
                    print("get lyric!!!!!!!!!")
                    print(lyric)
                    music.tag.lyrics.set(lyric)
                    music.tag.save()
                    if savepath:
                        try:
                            with open('{savepath}/{artist}-{name}.lrc'
                                              .format(savepath=savepath, artist=str(artist), name=str(title)), 'w') \
                                    as lrcfile:
                                lrcfile.write(lyric)
                        except Exception as e:
                            print(e)

    print('the end!')
