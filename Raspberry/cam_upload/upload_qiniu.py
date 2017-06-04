#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: upload_qiniu.py
@time: 2017/5/13 上午10:30
"""

import time
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import os

access_key = os.environ.get('QINIU_ACCESSKEY')
secret_key = os.environ.get('QINIU_SECRETKEY')

q = Auth(access_key, secret_key)

localfile = 'current_photo.jpg'

bucket_name = 'mypi'
key = '%s_%s_%s_%s_%s_%s.jpg' % (
    time.localtime()[0], time.localtime()[1], time.localtime()[2], time.localtime()[3], time.localtime()[4],
    time.localtime()[5])
if os.path.exists(localfile):
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = put_file(token, key, localfile)
    os.remove(localfile)
else:
    print("No such file or directory " + localfile)
