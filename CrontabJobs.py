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
from scapy.all import *
import datetime

if not os.path.exists('./temps'):
    os.mkdir('temps')


def get_time_str():
    t = datetime.datetime.now().strftime('%Y年%m月%d日%H点%M分')
    return t


def play_sound(d):
    s = TextToSound()

    n = './temps/123.mp3'
    r = s.convert_to_sound(d, path=n)
    if r:
        os.system(' mplayer {path}'.format(path=n))


def weather_broadcast():
    weather = GetWeather('上海')
    d = weather.getweather()

    t = get_time_str()
    d = '现在时间是{time},{weather},又是一天新的开始，fuck'.format(time=t, weather=d)
    play_sound(d)


def check_back():
    ipscan = '192.168.21.0/24'

    def write_run_log(s):
        with open('./temps/runlog.txt', 'w') as file:
            file.write(s)

    def get_run_log():
        with open('./temps/runlog.txt', 'r') as file:
            s = file.readline()
            return s

    try:
        ans, unans = srp(Ether(dst="F0:99:BF:E8:F9:1F") / ARP(pdst=ipscan), timeout=20, iface='eth0', verbose=False)
    except Exception, e:
        print str(e)
    else:
        """
        for snd, rcv in ans:
            s = get_run_log()
            print s
            if s == '1':
                return
            else:
                list_mac = rcv.sprintf("%Ether.src% - %ARP.psrc%")
                print list_mac
                d = '欢迎回来，亮亮。'
                play_sound(d)
                # list_mac = rcv.sprintf("%Ether.src% - %ARP.psrc%")
                # print list_mac
        """
        if ans and len(ans):

            s = get_run_log()
            print s
            if s == '1':
                return
            d = '欢迎回来，亮亮。'
            write_run_log('1')
            play_sound(d)

        else:
            write_run_log('0')
            return


if __name__ == '__main__':

    command = sys.argv[1]
    if command == 'weather':
        weather_broadcast()
    if command == 'checkback':
        check_back()
