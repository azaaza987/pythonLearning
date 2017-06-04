#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: client.py
@time: 2017/5/22 下午9:27
"""

import io
import socket
import struct
import time
import picamera
import datetime

client_socket = socket.socket()
client_socket.connect(('192.168.21.120', 8002))

connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    # camera.led = False
    camera.start_preview()
    time.sleep(2)

    start = time.time()
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        s = struct.pack('<L', stream.tell())
        print(s)
        connection.write(s)
        connection.flush()

        stream.seek(0)
        connection.write(stream.read())
        """
        if time.time() - start > 30:
            break
        """
        stream.seek(0)
        stream.truncate()

    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
