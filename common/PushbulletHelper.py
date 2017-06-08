#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliang
@license: Apache Licence 
@contact: liangliangyy@gmail.com
@site: http://www.lylinux.org
@software: PyCharm
@file: PushbulletHelper.py
@time: 2016/1/9 9:58
"""

api_key='o.fqiZCEeLH59spGOirrByYY6ZaOlOq3OE'

from pushbullet import Pushbullet

class PushbullectHelper():
    def __init__(self):
        self.pb=Pushbullet(api_key)
        self.iphone=self.pb.devices[0]
        self.device=self.pb.devices

    def sendnote(self,title,str):
        self.pb.push_note(title,str,device=self.iphone)
    def sendall(self,title,str):
        self.pb.push_note(title,str)
    def sendfile(self,file,name):
        filedata=self.pb.upload_file(file,name)
        self.pb.push_file(**filedata)