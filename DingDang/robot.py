#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: robot.py
@time: 2018/1/20 下午4:01
"""

import logging
import os
from DingDang.apis.tuling import TuLing
from DingDang.mic import Mic
from DingDang.apis.tts_stt import SoundToText
import log


class RoBot():
    def __init__(self):
        self.tuling = TuLing()
        self.mic = Mic()
        self.tts = SoundToText()

    def run(self):
        recordfile = self.mic.record()
        text = self.tts.convert_to_text(recordfile)

        rsp = self.tuling.getdata(text)
        self.mic.say(rsp)


if __name__ == '__main__':
    logger = log.setup_custom_logger('root')
    logger.debug('main message')

    robot = RoBot()
    while 1:
        robot.run()
