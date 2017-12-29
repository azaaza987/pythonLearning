#!/usr/bin/env python

import sys

sys.path.append('./')
import zipimport

importer = zipimport.zipimporter('jieba.mod')
jieba = importer.load_module('jieba')
import jieba.analyse


def search_keywords(self, content, topK=20):
    tags = jieba.analyse.extract_tags(content, topK=topK)
    return self.count_words(tags)


for line in sys.stdin:
    line = line.strip()
    results = search_keywords(line, 100)
    resultdict = dict()
    for s in results:
        if s and s.strip():
            if s in resultdict:
                resultdict[s] += 1
            else:
                resultdict[s] = 1

    if resultdict and len(resultdict):
        for s in resultdict:
            if s:
                print('%s\t%s' % (s, resultdict[s]))
