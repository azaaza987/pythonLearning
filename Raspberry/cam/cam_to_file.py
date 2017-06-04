#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: cam_to_file.py
@time: 2017/5/22 下午9:46
"""

import picamera
import datetime
import os

videoname = 'my_video.h264'
if os.path.exists(videoname):
    os.remove(videoname)

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.start_recording('my_video.h264')
camera.wait_recording(60)
camera.stop_recording()
exportfilename = datetime.datetime.now().strftime('%y_%m_%d_%H_%m_%s.mp4')
diskpath = '/var/nsa/disk/NoNameDisk/Raspberry/cam/'
os.system('ffmpeg -i {video} {export}'.format(video=videoname, export=exportfilename))

os.system('mv {export} {disk}'.format(export=exportfilename, disk=diskpath))
