#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: text_to_sound.py
@time: 2017/6/4 上午9:18
"""

import requests
import json
from BaiduAPI import GetWeather
import datetime
from urllib import urlencode
import wave
import base64
import json


class BaiDuYuYin():
    def __init__(self):
        self.appid = '9718832'
        self.appkey = 'yIPPoy516gjYTaSjy3fqRp11'
        self.secretkey = 'd5a3ab10561f1f732839b18caab47403'

    def get_accesstoken(self):
        url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={clientid}&client_secret={clientsecret}'.format(
            clientid=self.appkey, clientsecret=self.secretkey)
        rsp = requests.get(url=url)
        obj = json.loads(s=rsp.text, encoding='utf-8')
        return str(obj['access_token'])


class SoundToText(BaiDuYuYin):
    def convert_to_text(self, path):
        token = self.get_accesstoken()
        signal = open(path, "rb").read()
        speech_length = len(signal)
        speech = base64.b64encode(signal).decode("utf-8")
        s = {
            "format": "wav",
            'rate': 16000,
            'channel': 1,
            'cuid': 'fff',
            'token': token,
            'lan': 'zh',
            'speech': speech,
            'len': speech_length
        }

        url = 'http://vop.baidu.com/server_api'

        data_length = len(json.dumps(s).encode("utf-8"))

        headers = {"Content-Type": "application/json",
                   "Content-Length": str(data_length)}
        r = requests.post(url, data=json.dumps(s), headers=headers)
        d = json.loads(r.text)
        try:
            print str(d["result"][0])
            return d["result"][0]
        except:
            return "服务器出错。。。"


class TextToSound(BaiDuYuYin):
    def convert_to_sound(self, text, path):
        token = self.get_accesstoken()
        s = {
            'tex': text,
            'lan': 'zh',
            'tok': token,
            'ctp': 1,
            'cuid': '123fg31df',
            'spd': '3',
            'pit': '4',
            'vol': '5',
            'per': '0'
        }
        url = 'http://tsn.baidu.com/text2audio'
        rsp = requests.post(url, data=s)
        if rsp.headers['Content-Type'] == 'audio/mp3':
            with open(path, 'wb') as file:
                file.write(rsp.content)
                return True
        return False


if __name__ == '__main__':
    s = SoundToText()
    s.convert_to_text('record.wav')
    """
    s = TextToSound()
    weather = GetWeather('上海')
    d = weather.getweather()
    print(d)
    t = datetime.datetime.now().strftime('%Y年%m月%d日%H点%m分')
    d = '现在时间是{time},{weather},又是一天新的开始，fuck'.format(time=t, weather=d)
    s.convert_to_sound(d, path='123.mp3')
    """
