#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: server.py
@time: 2017/5/22 下午9:25
"""

import socket
import struct
from PIL import Image
import numpy
import io
import logging
import socketserver
from threading import Condition
from http import server

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8002))
server_socket.listen(0)

connection = server_socket.accept()[0].makefile('rb')

PAGE = """\
<html>
<head>
<title>camera MJPEG streaming demo</title>
</head>
<body>
<h1>Camera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


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

            while True:
                try:
                    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                    print(image_len)
                    if not image_len:
                        break

                    image_stream = io.BytesIO()
                    image_stream.write(connection.read(image_len))

                    image_stream.seek(0)
                    image = Image.open(image_stream)
                    cv2img = numpy.array(image, dtype=numpy.uint8)
                    imgbuffer = image_stream.getvalue()
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(imgbuffer))
                    self.end_headers()
                    self.wfile.write(imgbuffer)
                    self.wfile.write(b'\r\n')


                except Exception as e:
                    logging.warning(
                        'errror streaming client %s: %s',
                        self.client_address, str(e))

        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


output = StreamingOutput()

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
except Exception as e:
    print(e)
