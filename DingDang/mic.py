#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: mic.py
@time: 2018/1/20 下午3:29
"""

import pygame
from DingDang.apis.tts_stt import TextToSound, SoundToText
import logging
from pygame import mixer
import time

import wave, pyaudio
import tempfile

logger = logging.getLogger('root')


class RecordWav():
    def __init__(self):
        # Settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 16000
        self.CHANNELS = 1
        self.RECORD_SECONDS = 3

    def recordWave(self, path):
        pa = pyaudio.PyAudio()
        stream = pa.open(format=self.FORMAT,
                         channels=self.CHANNELS,
                         rate=self.RATE,
                         input=True,
                         frames_per_buffer=self.CHUNK)

        logger.info("recording...")
        buffer = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            audio_data = stream.read(self.CHUNK)
            buffer.append(audio_data)

        logger.info("record done")
        stream.stop_stream()
        stream.close()
        pa.terminate()

        wf = wave.open(path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(pa.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(buffer))
        wf.close()


mixer.init()


class Mic():
    def __init__(self):
        self.tts = TextToSound()
        self.stt = SoundToText()
        self.recorder = RecordWav()

    def say(self, text):
        # text = str(text).encode('utf-8').decode('utf-8')
        logger.info('DingDang Say:' + text)
        file = self.tts.convert_to_sound(text)
        if file:
            mixer.music.load(file)
            mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
        else:
            logger.critical('转换失败:' + text)

    def record(self):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as f:
            name = f.name
        self.recorder.recordWave(name)
        return name


if __name__ == '__main__':
    m = Mic()
    m.say('你好呀')
