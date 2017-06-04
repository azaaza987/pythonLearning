#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: Client.py.py
@time: 2017/5/14 下午3:37
"""

import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import picamera
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

ser_address = ('192.168.21.120', 10218)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.connect(ser_address)
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # show the frame
    # cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    data = image.tostring()
    clientsocket.send(data)
    #clientsocket.send(data, ser_address)
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
"""

connection = clientsocket.makefile('wb')

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 24
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)
    # Start recording, sending the output to the connection for 60
    # seconds, then stop
    camera.start_recording(connection, format='h264')
    camera.wait_recording(60)
    camera.stop_recording()
"""
while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("L", len(data)) + data)
