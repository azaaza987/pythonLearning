#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: hivedemo.py
@time: 2017/11/5 下午3:00
"""

from pyhive import hive

cursor = hive.connect(host='myhadoop', auth='NOSASL', database='default').cursor()
cursor.execute('select * from users limit 10')
print(cursor.fetchone())
print(cursor.fetchall())
for i in range(7, 10):
    sql = "insert into users VALUEs ({},'username{}')".format(i, str(i))
    cursor.execute(sql)
