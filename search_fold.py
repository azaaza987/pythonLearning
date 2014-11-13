###扫描本地音乐文件.并将歌词嵌入到音乐文件标签中

import threading
import time
import datetime
import re
import os
import eyed3
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def getstr(i):
    if i <10:
        return "0"+str(i)
    else:
        return str(i)

#musicpath=r'I:\music'
musicpath=r'F:\CloudMusic'

lrcpath=r'E:\lrc'



def deallrc(str):
    mystr=re.sub(r'\[\d\d:\d\d.\d\d\]','',str)
    mystr.replace('\n','')
    return mystr
    


def checklrcfile(path,timespan):
    file=open(path,'r')
    mylrcstr=''
    #print timespan
    for line in file.readlines(100):
        #errorlog(line)
        if line.find(timespan)>0:
            return deallrc(line)
        else:
            continue
    return ''

        
def getlrcstr(lrc):
    mylrcstr=''
    #print lrc
    for i in range(00,05):
        for j in range(00,59):
            for k in range(00,99):
                timespan=getstr(i)+":"+getstr(j)+"."+getstr(k)
                mylrcstr+=checklrcfile(lrc, timespan) 
            #print timespan
    return mylrcstr


def getlrc(musicname):
    musicname=u''.join(musicname)
    musicname=musicname.encode('gb2312')
    for root,dirs,files in os.walk(lrcpath):
        for filepath in files:
            the_path = os.path.join(root,filepath)
            if (the_path.find(musicname) != -1):
                print the_path
                return the_path

def errorlog(path):
    file=open(r'e:\nolrc.txt','a')
    if path is None:
        path=''
    path=path+'\n'
    file.write(path)
    file.close()

def writetag(themusic,lrcstr):
    music=eyed3.load(themusic)
    lrcstr=lrcstr.decode('utf8')
    lrcstr=u''.join(lrcstr)
    #lrcstr=unicode(lrcstr)
    music.tag.lyrics.set(lrcstr)
    music.tag.save()
    
    


def dealmusic(path):
    print path
    the_music = eyed3.load(path)
    the_teg = the_music.tag._getAlbum()
    the_artist = the_music.tag._getArtist()
    the_title = the_music.tag._getTitle()
    #print the_title
    
    try:
        lrc=getlrc(the_title)
        lrcstr=getlrcstr(lrc)
        writetag(path, lrcstr)  
    except:
        errorlog(path)
      
                    

class writelrc(threading.Thread):
    def __init__(self,the_path):
        threading.Thread.__init__(self)
        self.thepath=the_path
    def run(self):
        dealmusic(self.thepath)


if __name__=='__main__':
    count=0
    threads=[]
    for root,dirs,files in os.walk(musicpath):
            for filepath in files:
                the_path = os.path.join(root,filepath)
                if (the_path.find("mp3") != -1):
                    count+=1
                    
                    threads.append(writelrc(the_path))
    for t in threads:
        t.start()
    for t in threads:
        t.join()    
        """if count%10==0:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            threads=[]   """                       
                    
