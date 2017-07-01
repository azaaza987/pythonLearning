#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: tuling.py
@time: 2017/6/17 下午6:31
"""
import requests
import json


class TuLing():
    def __init__(self):

        self.__key__ = '2f1446eb0321804291b0a1e217c25bb5'
        self.__requrl__ = 'http://www.tuling123.com/openapi/api'

    def getdata(self, info):
        print info

        data = {
            'key': self.__key__,
            'info': info,
            'loc': '上海市浦东新区',
            'userid': '123'
        }
        rsp = requests.post(self.__requrl__, data=data)
        text = rsp.text
        jsons = json.loads(text, encoding='utf-8')
        if jsons["code"] and str(jsons["code"]) == '100000':
            return jsons["text"].encode('utf-8')
        else:
            return "服务器出错."


if __name__ == '__main__':
    tuling = TuLing()
    s = tuling.getdata('明天什么天气')
    from text_to_sound import TextToSound
    import os

    d = TextToSound()
    d.convert_to_sound(text=s, path='test.wav')
    os.system(' mplayer test.wav ')
