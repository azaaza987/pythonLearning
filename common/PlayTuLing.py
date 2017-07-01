#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: PlayTuLing.py
@time: 2017/6/17 下午6:52
"""

from tuling import TuLing
from RecordWav import RecordWav
from text_to_sound import TextToSound, SoundToText
import os


def startplay():
    path = 'play.wav'
    path2 = 'play2.wav'
    tuling = TuLing()
    r = RecordWav()
    t = TextToSound()
    s = SoundToText()
    r.recordWave(path)
    text = s.convert_to_text(path)
    print text
    info = tuling.getdata(info=text)
    print info
    t.convert_to_sound(text=info, path=path2)
    os.system('mplayer play2.wav')


while True:
    print 'start play'
    startplay()
