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

import os
import sys
import scapy
import struct
import pyping
import datetime

if not os.path.exists('./temps'):
    os.mkdir('temps')


def write_crontab_run_log(s):
    t = get_time_str()
    l = t + '  ' + s + '\n'
    with open('./temps/crontablog.log', 'a') as file:
        file.write(l)


def get_time_str():
    t = datetime.datetime.now().strftime('%Y年%m月%d日%H点%M分')
    return t


def play_sound(d):
    os.system('/home/pi/Linux_voice_1.109/bin/tts_sample {text} /home/pi/temps/sound.wav'.format(text=d))
    os.system('mplayer /home/pi/temps/sound.wav ')
    pass
    """
    s = TextToSound()

    n = './temps/123.mp3'
    r = s.convert_to_sound(d, path=n)
    if r:
        os.system(' mplayer {path}'.format(path=n))
    """


def play_voice(path):
    os.system(' mplayer {path}'.format(path=path))


def weather_broadcast():
    weather = GetWeather('上海')
    d = weather.getweather()

    t = get_time_str()
    d = '现在时间是{time},{weather}'.format(time=t, weather=d)
    play_sound(d)
    play_voice('/home/pi/voice/morning.m4a')


def check_back():
    ipscan = '192.168.21.66'

    def write_run_log(s):
        with open('./temps/runlog.txt', 'w') as file:
            file.write(s)

    def get_run_log():
        if not os.path.exists('./temps/runlog.txt'):
            os.system('touch ./temps/runlog.txt ')
        with open('./temps/runlog.txt', 'r') as file:
            s = file.readline()
            return s

    response = pyping.ping(ipscan, count=10)

    if response and response.avg_rtt and float(response.avg_rtt) >= 1:
        print response.avg_rtt
        s = get_run_log()
        print s
        if s == '1':
            write_crontab_run_log('get device not run')
            return

        write_run_log('1')
        write_crontab_run_log('start play')
        path = '/home/pi/voice/back.m4a'
        play_voice(path)
    else:
        write_crontab_run_log('not get')
        write_run_log('0')
        return


if __name__ == '__main__':

    command = sys.argv[1]
    if command == 'weather':
        weather_broadcast()
    if command == 'checkback':
        check_back()
