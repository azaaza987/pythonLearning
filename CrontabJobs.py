#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: CrontabJobs.py
@time: 2017/6/4 上午9:57
"""
from  common.text_to_sound import TextToSound
from common.BaiduAPI import GetWeather
import datetime
import os


def weather_broadcast():
    s = TextToSound()
    weather = GetWeather('上海')
    d = weather.getweather()
    print(d)
    t = datetime.datetime.now().strftime('%Y年%m月%d日%H点%m分')
    d = '现在时间是{time},{weather},又是一天新的开始，fuck'.format(time=t, weather=d)
    if not os.path.exists('./temps'):
        os.mkdir('temps')
    n = './temps/123.mp3'
    r = s.convert_to_sound(d, path=n)
    if r:
        os.system(' mplayer {path}'.format(path=n))


if __name__ == '__main__':
    weather_broadcast()
