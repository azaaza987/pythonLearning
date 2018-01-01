#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: spiro.py
@time: 2017/7/8 下午2:48
"""

import math
import turtle


def drawCircleTurtle(x, y, r):
    turtle.up()
    turtle.setpos(x + r, y)
    turtle.down()
    for i in range(0,365,5):
        a=math.radians(i)
        turtle.setpos(x+r*math.cos(a),y+r*math.sin(a))

if __name__ == '__main__':
    drawCircleTurtle(100, 100, 50)
    turtle.mainloop()
