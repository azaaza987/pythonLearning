# -*- coding: UTF-8 -*-

import socket, time
import pygame
from pygame.locals import *
from sys import exit

# 服务器地址，初始化socket
ser_address = ('localhost', 10218)
cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 设置超时
cli_socket.settimeout(5)

# 向服务器发送消息，并判断接收时是否超时，若超时则重发
while 1:
    cli_socket.sendto('startCam', ser_address)
    try:
        message, address = cli_socket.recvfrom(2048)
        if message == 'startRcv':
            print message
            break
    except socket.timeout:
        continue

cli_socket.recvfrom(65536)

# 初始化视频窗口
pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('Web Camera')
pygame.display.flip()

# 设置时间，可以用来控制帧率
clock = pygame.time.Clock()


# 主循环，显示视频信息
while 1:
    try:
        data, address = cli_socket.recvfrom(65536)
    except socket.timeout:
        continue
    camshot = pygame.image.frombuffer(data, (160,120), 'RGB')
    camshot = pygame.transform.scale(camshot, (640, 480))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cli_socket.sendto('quitCam', ser_address)
            cli_socket.close()
            pygame.quit()
            exit()
    screen.blit(camshot, (0,0))
    pygame.display.update() 
    clock.tick(20)
