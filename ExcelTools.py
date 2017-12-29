#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: ExcelTools.py
@time: 2017/10/9 下午10:04
"""

import xlrd

data = xlrd.open_workbook('/Users/liangliang/data.xls')
table = data.sheets()[0]

nrows = table.nrows
ncols = table.ncols
"""
for i in range(nrows):
    print(table.row_values(i))
"""

areas = table.col_values(2)
areas.remove('覆盖区域')
areas = list(set(areas))
print(areas)
