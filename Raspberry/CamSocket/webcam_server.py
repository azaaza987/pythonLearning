#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: webcam_server.py
@time: 2017/5/22 下午10:41
"""

import io
import socket
import struct
from PIL import Image
import io
import logging
import socketserver
from threading import Condition
from http import server

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8003))
server_socket.listen(0)
PAGE = """\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

connection = server_socket.accept()[0].makefile('rb')

datas = []


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:

                    image_stream = io.BytesIO()

                    image_stream.write(connection.read(34507))

                    image_stream.seek(0)
                    s = image_stream.read()
                    datas.append(s)

                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', 172504)
                    self.end_headers()
                    self.wfile.write(s)
                    self.wfile.write(b'\r\n')
            finally:
                connection.close()
                server_socket.close()
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


try:
    address = ('', 8001)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()

finally:
    pass
