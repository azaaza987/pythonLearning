#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: noteplayer.py
@time: 2017/7/8 下午3:05
"""
import numpy as np
import sys, os
import time, random
import wave, pygame
from collections import deque

nChannels = 1
sampleWidth = 2
frameRate = 44100
nFrames = 44100


def writewav(fname, data):
    file = wave.open(fname, 'wb')

    file.setparams((nChannels, sampleWidth, frameRate, nFrames, "NONE", 'noncompressed'))
    file.writeframes(data=data)
    file.close()


def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate / freq)
    buf = deque([random.random() - 0.5 for i in range(N)])
