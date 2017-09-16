#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: ReSetMusicPath.py
@time: 2017/9/16 下午9:42
"""

'''
整理音乐文件夹->演唱者/专辑/音乐
'''

import eyed3
import os, sys
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='音乐路径', dest='musicpath')
parser.add_argument('-s', '--savepath', help='保存路径', dest='savepath')
args = parser.parse_args()
musicpath = args.musicpath
savepath = args.savepath

if __name__ == '__main__':
    if savepath:
        if not os.path.exists(path=savepath):
            print('歌词保存路径不存在')
            sys.exit(0)
    if not musicpath:
        print('音乐文件不存在')
        sys.exit(0)
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    for root, dirs, files in os.walk(musicpath):
        for filepath in files:
            the_path = os.path.join(root, filepath)
            if (the_path.find("mp3") != -1):
                music = eyed3.load(the_path)
                artist = music.tag._getArtist()
                title = music.tag._getTitle()
                album = music.tag._getAlbum()
                p = '{savepath}/{artist}/{album}/'.format(savepath=savepath, artist=artist, album=album)
                if not os.path.exists(p):
                    os.makedirs(p)
                if the_path != p + filepath:
                    shutil.copy(the_path, p + filepath)
