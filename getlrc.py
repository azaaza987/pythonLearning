# -*- coding: utf-8 -*-

#扫描本地音乐 从百度下载歌词到本地

import os
import os.path
import re
import eyed3
import urllib2
import urllib
from urllib import urlencode
import sys 

import os
reload(sys) 
sys.setdefaultencoding('utf8')

#music_path = r"F:\CloudMusic"
music_path=r'e:\music'
lrc_path = r"e:\lrc"

#os.remove('nolrc.txt')
#os.remove('lrcxml.txt')

the_file = open('lrcxml.txt','a')
nolrc_file = open('nolrc.txt','a')

for root,dirs,files in os.walk(music_path):
    for filepath in files:
        the_path = os.path.join(root,filepath)
        try:
            if (the_path.find("mp3") != -1):
                print the_path
                the_music = eyed3.load(the_path)
                the_teg = the_music.tag._getAlbum()
                the_artist = the_music.tag._getArtist()
                the_title = the_music.tag._getTitle()
               # print the_teg
               # print the_title
               # print the_artist
                b = str(the_title).replace(' ','+')
               # print b
                a = the_artist.replace(' ','+')
                
                print a
                print b
                #print urlencode(str(b))
                if isinstance(a,unicode):
                    a = a.encode('utf8')
                song_url = "http://box.zhangmen.baidu.com/x?op=12&count=1&title="+b+"$$"+a+"$$$$ "
                #song_url = "http://mp3.baidu.com/dev/api/?tn=getinfo&ct=0&word="+b+"ie=utf-8&format=xml"
                #print song_url
                the_file.write(song_url+'\n')
                page = urllib2.urlopen(song_url).read()
                #print page
                theid = 0
                
                lrcid =  re.compile('<lrcid>(.*?)</lrcid>',re.S).findall(page)
                have_lrc = True
                if lrcid != []:
                    theid = lrcid[0]
                    
                else:
                    nolrc_file.write(the_title+'\n')
                    have_lrc = False
                print theid
                
                
                if have_lrc:
                    firstid = int(theid)/100
                    lrcurl = "http://box.zhangmen.baidu.com/bdlrc/"+str(firstid)+"/"+theid+".lrc"
                    print lrcurl
                    lrc = urllib2.urlopen(lrcurl).read()
                    if(lrc.find('html')== -1):
                        lrcfile = open(lrc_path+"\\"+the_title+".lrc",'w')
                        lrcfile.writelines(lrc)
                        lrcfile.close()
                    else:
                        nolrc_file.write(the_title+'\n')
        except:
            pass
                
the_file.close()
nolrc_file.close()
print "end!"