#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: Apache Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: BaiduAPI.py
@time: 2016/10/21 下午11:54
"""

import sys, urllib, urllib2, json
import hashlib
from CommonHelper import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseApi():
    def __init__(self, apikey=None):
        if apikey:
            self.apikey = apikey
        else:
            self.apikey = '8dd1326fc4b271db91e03dba3d84b427'

    def UserAgent(self, url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
                     "Referer": 'http://baidu.com/'}

        req = urllib2.Request(url, headers=i_headers)
        req.add_header("apikey", self.apikey)
        html = urllib2.urlopen(req).read()
        return html

    def UserAgent2(self, url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
                     "Referer": 'http://baidu.com/',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                     }

        req = urllib2.Request(url)

        html = urllib2.urlopen(req).read()
        return html


apikey = '8dd1326fc4b271db91e03dba3d84b427'


class GetWeather(BaseApi):
    def __init__(self, city):

        BaseApi.__init__(self, apikey)
        self.city = city

    def getweather(self):
        try:
            p = {
                'city': self.city,
                'key': 'd9b3201a8c8842a59e2dacb94f7fe12d'
            }

            url = 'https://free-api.heweather.com/x3/weather?' + urllib.urlencode(p)
            content = self.UserAgent2(url)
            # print content
            encodejson = json.loads(content, encoding='utf-8')
            dayinfo = encodejson['HeWeather data service 3.0'][0]['daily_forecast'][0]
            dayweather = dayinfo['cond']['txt_d']
            maxtmp = dayinfo['tmp']['max']
            mintmp = dayinfo['tmp']['min']
            # print str(mintmp)#.decode("unicode-escape")
            info = u"" + self.city + "天气:" + dayweather + ",最高温度:" + maxtmp + "度,最低温度:" + mintmp + "度";
            print(info)
            return info

        except Exception, e:
            print(e)
            return self.getweather()


class GetJoke(BaseApi):
    def __init__(self):
        self.badwords = [

            u"床",
            u"性",

            u"嘿",

            u"j",
            u"J",
            u"云雨",
            u"撸",
            u"公安",
            u"人民币",
            u"中国",
            u"寡妇",
            u"媳妇",
            u"高潮",
        ]

        BaseApi.__init__(self, apikey)
        self.requrl = "http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_text"
        self.jokeindex = 1

    def __CheckBadWorld(self, content, bad):
        # content = str(content)
        return content.find(bad) >= 0

    def getjoke(self, page):
        content = self.__getjoke__(page).replace(' ', '')
        encodejson = json.loads(content, encoding='utf-8')
        # encodejson = str(encodejson)
        return encodejson

    def GetJokeContent(self):
        try:
            joke = self.getjoke(self.jokeindex)
            haserr = False
            for j in joke['showapi_res_body']['contentlist']:
                content = j["text"]
                for bad in self.badwords:
                    if self.__CheckBadWorld(content.encode('utf-8'), bad.encode('utf-8')):
                        haserr = True

            if not haserr:
                finalljoke = content.encode('utf-8')
                # print finalljoke
                return finalljoke
            else:
                self.jokeindex += 1
                return self.GetJokeContent()

        except Exception as e:
            # writefile(e.message)
            print(str(e.message))
            return self.GetJokeContent()

    def __getjoke__(self, page):
        url = self.requrl + "?page=" + str(page)
        res = self.UserAgent(url)
        return res


class GetWisdomWords(BaseApi):
    def __init__(self):
        BaseApi.__init__(self, apikey)
        self.errorcount = 0
        self.__rediskey = 'wisdom'
        self.requrl = 'http://apis.baidu.com/txapi/dictum/dictum'

    def getWisdomWords(self):
        try:
            if self.errorcount > 10:
                return 'error'
            self.errorcount += 1
            rsp = self.UserAgent(self.requrl)
            print rsp
            data = json.loads(rsp, encoding='utf-8')

            content = data['newslist'][0]['content']
            mrname = data['newslist'][0]['mrname']
            print content
            result = mrname + " : " + content
            """
            if len(result) > 150:
                return self.getWisdomWords()
            """
            md5 = StringHelper.GetMD5(result.encode('utf-8'))

            redishelper = RedisHelper()
            if redishelper.sset(self.__rediskey, md5) == 1:
                return result
            else:
                return self.getWisdomWords()

        except Exception, e:
            print 'error:wisdom' + str(e.message)
            return self.getWisdomWords()


if __name__ == '__main__':
    weather = GetWeather('珠海')
    weather.getweather()
