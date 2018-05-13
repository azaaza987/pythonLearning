#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: tuling.py
@time: 2018/1/20 下午4:03
"""

import requests
import json
import logging

logger = logging.getLogger('root')


class TuLing():
    def __init__(self):

        self.__key__ = '2f1446eb0321804291b0a1e217c25bb5'
        self.__requrl__ = 'http://www.tuling123.com/openapi/api'

    def getdata(self, info):

        data = {
            'key': self.__key__,
            'info': info,
            'loc': '上海市浦东新区',
            'userid': '123'
        }
        rsp = requests.post(self.__requrl__, data=data)
        text = rsp.text
        logger.info(text)
        jsons = json.loads(text, encoding='utf-8')
        if jsons["code"] and str(jsons["code"]) == '100000':
            return str(jsons["text"])
        else:
            logger.error(text)
            return "服务器出错."


if __name__ == '__main__':
    tuling = TuLing()
    rsp = tuling.getdata('你好呀')
    print(rsp)
