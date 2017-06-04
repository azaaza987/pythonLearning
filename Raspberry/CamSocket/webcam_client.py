#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: webcam_client.py
@time: 2017/5/22 下午10:41
"""

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

import io
import socket
import struct
import time
import picamera
import datetime

client_socket = socket.socket()
client_socket.connect(('192.168.21.120', 8003))
connection = client_socket.makefile('wb')


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
        self.stream = None

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.stream = self.buffer
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    while True:
        with output.condition:
            output.condition.wait()
            # frame = output.frame
            # size = len(frame)
            stream = output.stream


            stream.seek(0)
            print(len(stream.read()))
            connection.write(stream.read())
            """
            if time.time() - start > 30:
                break
            """
            stream.seek(0)
            stream.truncate()
