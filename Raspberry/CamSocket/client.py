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
import datetime
import cv2

client_socket = socket.socket()
client_socket.connect(('192.168.21.120', 8002))

connection = client_socket.makefile('wb')
try:

    cap = cv2.VideoCapture(0)
    while (1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        # cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
            # break
        img_str = cv2.imencode('.jpg', frame)[1].tostring()

        s = struct.pack('<L', len(img_str))
        #print(s)
        connection.write(s)
        connection.flush()

        connection.write(img_str)
        connection.flush()

        #connection.write(struct.pack('<L', 0))
except Exception as e:
    print(e)
finally:
    connection.close()
    client_socket.close()
