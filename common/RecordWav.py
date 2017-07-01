#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: RecordWav.py
@time: 2017/6/17 下午6:43
"""

import wave, pyaudio


class RecordWav():
    def __init__(self):
        # Settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 16000
        self.CHANNELS = 1
        self.RECORD_SECONDS = 5

    # Record Function
    def recordWave(self, path):
        pa = pyaudio.PyAudio()
        stream = pa.open(format=self.FORMAT,
                         channels=self.CHANNELS,
                         rate=self.RATE,
                         input=True,
                         frames_per_buffer=self.CHUNK)

        print 'Recording...'

        buffer = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            audio_data = stream.read(self.CHUNK)
            buffer.append(audio_data)

        print 'Record Done'

        stream.stop_stream()
        stream.close()
        pa.terminate()

        wf = wave.open(path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(pa.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(buffer))
        wf.close()


if __name__ == '__main__':
    s = RecordWav()
    s.recordWave(path='record.wav')
