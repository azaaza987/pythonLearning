#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: api.py
@time: 2017/10/22 上午2:43
"""

import re
import os
import json
import time
import hashlib
import random
import base64
import binascii

from Crypto.Cipher import AES
from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup
import requests
from .utils import *
from .storage import Storage
import eyed3

default_timeout = 10


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


def geturl_new_api(song):
    br_to_quality = {128000: 'MD 128k', 320000: 'HD 320k'}
    alter = NetEase().songs_detail_new_api([song['id']])[0]
    url = alter['url']
    quality = br_to_quality.get(alter['br'], '')
    return url, quality


# 获取高音质mp3 url
def geturl(song):
    quality = 1
    if song['hMusic'] and quality <= 0:
        music = song['hMusic']
        quality = 'HD'
    elif song['mMusic'] and quality <= 1:
        music = song['mMusic']
        quality = 'MD'
    elif song['lMusic'] and quality <= 2:
        music = song['lMusic']
        quality = 'LD'
    else:
        return song['mp3Url'], ''

    quality = quality + ' {0}k'.format(music['bitrate'] // 1000)
    song_id = str(music['dfsId'])
    enc_id = encrypted_id(song_id)
    url = 'http://m%s.music.126.net/%s/%s.mp3' % (random.randrange(1, 3),
                                                  enc_id, song_id)
    return url, quality


class NetEase():
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
            # NOQA
        }
        self.cookies = {'appver': '1.5.2'}
        self.playlist_class_dict = {}
        self.session = requests.Session()
        self.storage = Storage()
        self.session.cookies = LWPCookieJar(self.storage.cookie_path)
        try:
            self.session.cookies.load()
            cookie = ''
            if os.path.isfile(self.storage.cookie_path):
                self.file = open(self.storage.cookie_path, 'r')
                cookie = self.file.read()
                self.file.close()
            expire_time = re.compile(r'\d{4}-\d{2}-\d{2}').findall(cookie)
            if expire_time:
                if expire_time[0] < time.strftime('%Y-%m-%d', time.localtime(time.time())):
                    self.storage.database['user'] = {
                        'username': '',
                        'password': '',
                        'user_id': '',
                        'nickname': '',
                    }
                    self.storage.save()
                    os.remove(self.storage.cookie_path)
        except IOError as e:
            print(e.strerror)
            self.session.cookies.save()

    def httpRequest(self,
                    method,
                    action,
                    query=None,
                    urlencoded=None,
                    callback=None,
                    timeout=None):
        connection = json.loads(
            self.rawHttpRequest(method, action, query, urlencoded, callback, timeout)
        )
        return connection

    def rawHttpRequest(self,
                       method,
                       action,
                       query=None,
                       urlencoded=None,
                       callback=None,
                       timeout=None):
        connection = None
        if method == 'GET':
            url = action if query is None else action + '?' + query
            connection = self.session.get(url,
                                          headers=self.header,
                                          timeout=default_timeout)

        elif method == 'POST':
            connection = self.session.post(action,
                                           data=query,
                                           headers=self.header,
                                           timeout=default_timeout)

        elif method == 'Login_POST':
            connection = self.session.post(action,
                                           data=query,
                                           headers=self.header,
                                           timeout=default_timeout)
            self.session.cookies.save()

        connection.encoding = 'UTF-8'
        return connection.text

    # 每日推荐歌单
    def recommend_playlist(self):
        try:
            action = 'http://music.163.com/weapi/v1/discovery/recommend/songs?csrf_token='  # NOQA
            self.session.cookies.load()
            csrf = ''
            for cookie in self.session.cookies:
                if cookie.name == '__csrf':
                    csrf = cookie.value
            if csrf == '':
                return False
            action += csrf
            req = {'offset': 0, 'total': True, 'limit': 20, 'csrf_token': csrf}
            page = self.session.post(action,
                                     data=encrypted_request(req),
                                     headers=self.header,
                                     timeout=default_timeout)
            results = json.loads(page.text)['recommend']
            song_ids = []
            for result in results:
                song_ids.append(result['id'])
            data = map(self.song_detail, song_ids)
            return [d[0] for d in data]
        except (requests.exceptions.RequestException, ValueError) as e:
            print(e.strerror)
            return False
            # song id --> song url ( details )

    def song_detail(self, music_id):
        action = 'http://music.163.com/api/song/detail/?id={}&ids=[{}]'.format(
            music_id, music_id)  # NOQA
        try:
            data = self.httpRequest('GET', action)
            return data['songs']
        except requests.exceptions.RequestException as e:
            print(e.strerror)
            return []
            # song ids --> song urls ( details )
            # 搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*

    def search(self, s, stype=1, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get'
        data = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        return self.httpRequest('POST', action, data)

    def search_by_artists_name(self, name, artists):
        results = self.search(name)
        if ('result' in results and results['result'] and 'songs' in results['result'] and results['result']['songs']):
            for s in results['result']['songs']:
                s_artists = s['artists'][0]['name']
                if artists == s_artists:
                    return s
        return None

    def get_artist_album(self, artist_id, offset=0, limit=50):
        action = 'http://music.163.com/api/artist/albums/{}?offset={}&limit={}'.format(
            artist_id, offset, limit)
        try:
            data = self.httpRequest('GET', action)
            return data['hotAlbums']
        except requests.exceptions.RequestException as e:
            print(e.strerror)
            return []

    # album id --> song id set
    def album(self, album_id):
        action = 'http://music.163.com/api/album/{}'.format(album_id)
        try:
            data = self.httpRequest('GET', action)
            return data['album']['songs']
        except requests.exceptions.RequestException as e:
            print(e.strerror)
            return []

    def songs_detail(self, ids, offset=0):
        tmpids = ids[offset:]
        tmpids = tmpids[0:100]
        tmpids = list(map(str, tmpids))
        action = 'http://music.163.com/api/song/detail?ids=[{}]'.format(  # NOQA
            ','.join(tmpids))
        try:
            data = self.httpRequest('GET', action)

            # the order of data['songs'] is no longer the same as tmpids,
            # so just make the order back
            data['songs'].sort(key=lambda song: tmpids.index(str(song['id'])))

            return data['songs']
        except requests.exceptions.RequestException as e:
            print(e.strerror)
            return []

    def songs_detail_new_api(self, music_ids, bit_rate=320000):
        action = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='  # NOQA
        self.session.cookies.load()
        csrf = ''
        for cookie in self.session.cookies:
            if cookie.name == '__csrf':
                csrf = cookie.value
        if csrf == '':
            print('You Need Login', 1)
        action += csrf
        data = {'ids': music_ids, 'br': bit_rate, 'csrf_token': csrf}
        connection = self.session.post(action,
                                       data=encrypted_request(data),
                                       headers=self.header, )
        result = json.loads(connection.text)
        return result['data']

        # lyric http://music.163.com/api/song/lyric?os=osx&id= &lv=-1&kv=-1&tv=-1

    def song_lyric(self, music_id):
        action = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(  # NOQA
            music_id)
        try:
            data = self.httpRequest('GET', action)
            if 'lrc' in data and 'lyric' in data['lrc'] and data['lrc']['lyric'] is not None:
                lyric_info = data['lrc']['lyric']
            else:
                lyric_info = '未找到歌词'
            return lyric_info
        except requests.exceptions.RequestException as e:
            print(e.strerror)
            return []

    def song_tlyric(self, music_id):
        action = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(  # NOQA
            music_id)
        try:
            data = self.httpRequest('GET', action)
            if 'tlyric' in data and data['tlyric'].get('lyric') is not None:
                lyric_info = data['tlyric']['lyric'][1:]
            else:
                lyric_info = '未找到歌词翻译'
            return lyric_info
        except requests.exceptions.RequestException as e:
            print(e.strerror)
            return []


def download_songs(song, savepath):
    name = song['name']
    artist = song['artists'][0]['name']
    album = song['album']['name']
    albumurl = song['album']['artist']['img1v1Url']
    savepath = '{s}/{ar}/{ab}'.format(s=savepath, ar=artist, ab=album)
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    id = song['id']
    ids = []
    ids.append(id)
    m = NetEase()
    url = geturl_new_api(m.songs_detail(ids)[0])
    print(url)
    ur = url[0]
    if ur:
        rsp = requests.get(ur)
        musicpath = savepath + '/' + name + '.mp3'
        with open(musicpath, 'wb') as file:
            file.write(rsp.content)
        imgcontent = requests.get(albumurl).content
        e = eyed3.load(musicpath)
        e.tag.artist = artist
        e.tag.album = album
        e.tag.title = name
        e.tag.album_artist = artist
        # e.tag.images.set(6, imgcontent, "image/jpeg", name)
        e.tag.images.set(6, imgcontent, "image/jpeg", 'Front cover')
        lyric = m.song_lyric(id)
        print(lyric)
        parser = LyricTools(lyric=lyric)
        lrcdict = parser.parse_lrc_to_dict()

        lrc = parser.parse_lyric_dict(lrcdict)
        e.tag.lyrics.set(lrc)
        e.tag.save()


if __name__ == '__main__':
    m = NetEase()
    # 431795900
    # print(geturl_new_api(m.songs_detail([431795900])[0]))  # MD 128k, fallback
    results = m.search('收敛水', 1)
    print(results)
    savepath = 'songs'
    if (results['result'] and results['result']['songs']):
        for s in results['result']['songs']:
            print(s)
            download_songs(s, savepath)
