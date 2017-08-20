#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: AnalyzeLyric.py
@time: 2017/8/20 下午12:38
"""

import jieba
import jieba.analyse
import os
import sys
import re
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import operator
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

lrcpath = '/Users/liangliang/Source/Python/python/Tools/AnalyzeMusic/Lyrics'

test_word = '我来到北京清华大学,我，不爱，清华，大学，北京，北京，清华大学，不喜欢'


class JieBaTools():
    def __init__(self):
        self.wordlist = []

    def wordcount(self, content):

        results = jieba.cut(content, cut_all=False)

        return self.count_words(results)

    def count_words(self, words):
        freq = {}
        for result in words:
            self.wordlist.append(result)
            if result in freq:
                freq[result] += 1
            else:
                freq[result] = 1
        return freq

    def search_keywords(self, content, topK=20):
        tags = jieba.analyse.extract_tags(content, topK=topK)
        return self.count_words(tags)


def generate_wordcloud2(word_list, maskname):
    from scipy.misc import imread
    text = ' '.join(word_list)
    color_mask = imread(maskname)  # 设置图云背景
    cloud = WordCloud(
        background_color='white',  # 设置背景颜色,默认颜色则为黑色
        font_path='PingFang.ttc',  # 中文图云必须指定字体，不然全是框框
        max_words=10000,  # 词云显示的最大词数
        # font_step=2,  # 字号的步调
        mask=color_mask,  # 设置背景图片
        random_state=15,  # 随机配色方案
        # min_font_size=5,  # 最小字号
        # max_font_size=100,  # 最大字号
        # stopwords={''},  # 设置词云中不想要显示的词
        # prefer_horizontal=0.1,  # 设置词云中水平显示的词的比例
        scale=2  # 生成图片与背景图片比例，默认为1
    )
    cloud.generate(text)  # 对分词后的文本生成词云
    image_colors = ImageColorGenerator(color_mask)  # 从背景图片获取颜色
    plt.show(cloud.recolor(color_func=image_colors))  # 词云中词的颜色按照背景中获取的颜色
    plt.imshow(cloud, cmap=plt.cm.gray)  # 以图片的形式显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 展示图片


def generate_wordcloud(word_list, mask_name):
    text = ' '.join(word_list)
    mask = np.array(Image.open(mask_name))

    wc = WordCloud(font_path='PingFang.ttc', background_color='white'  # , mask=mask
                   , scale=2, max_words=10000)

    wc.generate(text)

    image_colors = ImageColorGenerator(mask)

    plt.imshow(wc)
    plt.axis("off")
    # 绘制词云
    plt.figure()
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    # 绘制背景图片为颜色的图片
    plt.figure()
    plt.imshow(mask, cmap=plt.cm.gray)
    plt.axis("off")
    plt.show()


def ignore_punctuation(content):
    content = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！: ：，。？、~@#￥%……&*（）]+", "", content)
    return content


def search_lyrics(path):
    result = {}
    total_lines = 0
    tool = JieBaTools()
    for root, dirs, files in os.walk(path):
        for filepath in files:
            the_path = os.path.join(root, filepath)
            if (the_path.find("lrc") != -1):
                with open(the_path, 'r', encoding='utf-8') as lrcfile:
                    lines = lrcfile.readlines()
                    total_lines += len(lines)
                    for line in lines:
                        # lrc = ignore_punctuation(line)
                        lrc = line

                        counts = tool.search_keywords(lrc, 100)
                        # counts = tool.wordcount(lrc)
                        for f in counts:

                            if f in result:
                                result[f] += counts[f]
                            else:
                                result[f] = counts[f]
    s = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    """
    for r in s:
        print(r)
    """
    print(total_lines)
    generate_wordcloud(tool.wordlist, 'eason7.jpg')


if __name__ == '__main__':
    search_lyrics(lrcpath)
