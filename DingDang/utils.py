#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: utils.py
@time: 2018/1/20 下午3:13
"""

import os
from pydub import AudioSegment
import logging


def mp3_to_wav(mp3_file):
    target = mp3_file.replace(".mp3", ".wav")
    if os.path.exists(mp3_file):
        voice = AudioSegment.from_mp3(mp3_file)
        voice.export(target, format="wav")
        return target
    else:
        print(u"文件错误")
