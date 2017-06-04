#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: pygameserver.py
@time: 2017/5/14 下午10:28
"""

import socket, time
import pygame
from pygame.locals import *
from sys import exit
import time

# 服务器地址，初始化socket
ser_address = ('192.168.21.120', 10218)
ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind(ser_address)

# 初始化视频窗口
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Web Camera')
pygame.display.flip()

# 设置时间，可以用来控制帧率
clock = pygame.time.Clock()

# 主循环，显示视频信息
while 1:
    try:
        data, address = ser_socket.recvfrom(65536)
    except socket.timeout:
        print('time out')
        continue
    time.sleep(1)
    camshot = pygame.image.frombuffer(data, (160, 120), 'RGB')
    camshot = pygame.transform.scale(camshot, (640, 480))

    screen.blit(camshot, (0, 0))
    pygame.display.update()
    clock.tick(20)
