#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: Apache Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: client.py
@time: 2016/9/28 下午10:36
"""

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