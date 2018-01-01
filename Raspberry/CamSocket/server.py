#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: server.py
@time: 2017/5/22 下午9:25
"""

import io
import socket
import struct
from PIL import Image
import cv2
import numpy

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8002))
server_socket.listen(0)

connection = server_socket.accept()[0].makefile('rb')
try:
    while True:

        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        print(image_len)
        if not image_len:
            break

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        image_stream.seek(0)
        image = Image.open(image_stream)
        cv2img = numpy.array(image, dtype=numpy.uint8)
        print('Image is %dx%d' % image.size)
        image.save('test.jpg')
        cv2.imshow('frame', cv2img)
        cv2.waitKey(10)
finally:
    connection.close()
    server_socket.close()
