#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: Apache Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: server.py
@time: 2016/9/28 下午10:40
"""
import socket

ser_address = ('127.0.0.1', 8818)
ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind((ser_address))

while 1:
    message, address = ser_socket.recvfrom(2048)
    print address
    print message
    data = raw_input('input: ')
    ser_socket.sendto(data.encode(),address)