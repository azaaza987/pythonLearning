#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: Server2.py
@time: 2017/5/14 下午3:05
"""
import numpy as np
import cv2

import socket
import struct
import pickle

payload_size = struct.calcsize("L")

ser_address = ('127.0.0.1', 8818)
ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind((ser_address))

cap = cv2.VideoCapture(0)

while (True):
    message, address = ser_socket.recvfrom(2048)
    print address
    print message
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Our operations on the frame come here

    # Display the resulting frame
    cv2.imshow('frame', gray)

    data = pickle.dumps(frame)

    ser_socket.sendto( data[:1024000], address)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
