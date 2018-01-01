#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: image_to_ascil.py
@time: 2017/7/18 下午10:01
"""

from PIL import Image
import argparse

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
parser = argparse.ArgumentParser()
parser.add_argument('file')

args = parser.parse_args()

img = args.file


def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ''
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


im = Image.open(img)
width = int(im.width / 100)
height = int(im.height / 100)
im = im.resize((width, height), Image.NEAREST)
txt = ''
for i in range(height):
    for j in range(width):
        txt += get_char(*im.getpixel((j, i)))
    txt += '\n'

# print(txt)
with open('text.txt', 'w') as file:
    file.write(txt)
