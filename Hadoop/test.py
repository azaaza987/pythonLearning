#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: test.py.py
@time: 2017/11/4 下午11:31
"""

import zipimport
path='/home/hadoop/src/sources/jieba.mod'
importer = zipimport.zipimporter(path)
jieba = importer.load_module('jieba')
import jieba.analyse
