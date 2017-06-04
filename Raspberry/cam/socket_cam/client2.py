#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: client2.py
@time: 2017/5/14 下午3:03
"""

import socket, sys
import pygame
from PIL import Image

import socket


ser_address = ('127.0.0.1', 8818)

cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cli_socket.settimeout(5)
cli_socket.connect(ser_address)
cli_socket.send('start'.encode())

while 1:

    try:
        message, address = cli_socket.recvfrom(2048)
        print 'from server: '+message
        data=raw_input('input: ')
        cli_socket.send(data.encode())
    except Exception as e:
        print e.message
"""
# Create a var for storing an IP address:
ser_address = ('127.0.0.1', 8818)

cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cli_socket.settimeout(5)
cli_socket.connect(ser_address)
cli_socket.send('start'.encode())
# Start PyGame:
pygame.init()
screen = pygame.display.set_mode((320, 240))
pygame.display.set_caption('Remote Webcam Viewer')
font = pygame.font.SysFont("Arial", 14)
clock = pygame.time.Clock()
timer = 0
previousImage = ""
image = ""

# Main program loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

            # Receive data
    if timer < 1:

        data = cli_socket.recv(1024000)
        timer = 30

    else:
        timer -= 1
    previousImage = image

    # Convert image
    try:
        image = Image.frombytes("RGB", (120, 90), data)
        image = image.resize((320, 240))
        image = pygame.image.frombuffer(image.tostring(), (320, 240), "RGB")

    # Interupt
    except Exception, e:
        print e
        image = previousImage
    if image == '':
        continue
    output = image
    screen.blit(output, (0, 0))
    clock.tick(60)
    pygame.display.flip()
"""