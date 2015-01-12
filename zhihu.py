# -*- coding: utf-8 -*-
#抓取知乎个人收藏
import sys
reload(sys)  
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import cookielib
import string 
import re 
from bs4 import BeautifulSoup
from docx import Document
from docx import *
from docx.shared import Inches
from sys import exit


loginurl='http://www.zhihu.com/login'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',}  

postdata={
  '_xsrf':  'acab9d276ea217226d9cc94a84a231f7',
  'email':  'liangliangyy@gmail.com',
  'password': '*****',
  'rememberme':'y'    
}


mydoc=Document()
questiontitle=''
#----------------------------------------------------------------------
def  dealimg(imgcontent):
    soup=BeautifulSoup(imgcontent)
    try:
        for imglink in soup.findAll('img'):
            if imglink is not None :
                myimg= imglink.get('src')
                #print myimg
                if myimg.find('http')>=0:
                    imgsrc=urllib2.urlopen(myimg).read()
                    imgnamere=re.compile(r'http\S*/')
                    imgname=imgnamere.sub('',myimg)
                    #print imgname
                    with open(u'myimg'+'/'+imgname,'wb') as code:
                        code.write(imgsrc)
                        mydoc.add_picture(u'myimg/'+imgname,width=Inches(1.25))
    except:
        pass
    strinfo=re.compile(r'<noscript>[\s\S]*</noscript>')
    imgcontent=strinfo.sub('',imgcontent)
    return imgcontent
    




def enterquestionpage(pageurl):
    html=urllib2.urlopen(pageurl).read()
    soup=BeautifulSoup(html)
    questiontitle=soup.title.string
    mydoc.add_heading(questiontitle,level=3)
    for div in soup.findAll('div',{'class':'fixed-summary zm-editable-content clearfix'}):
        #print div
        conent=str(div).replace('<div class="fixed-summary zm-editable-content clearfix">','').replace('</div>','')
        
        conent=conent.decode('utf-8')
        conent=conent.replace('<br/>','\n')
        
        conent=dealimg(conent)
        mydoc.add_paragraph(conent,style='BodyText3')
        """file=open('222.txt','a')
        file.write(str(conent))
        file.close()"""
        
    




def entercollectpage(pageurl):
    html=urllib2.urlopen(pageurl).read()
    soup=BeautifulSoup(html)
    for div in soup.findAll('div',{'class':'zm-item'}):
        h2content=div.find('h2',{'class':'zm-item-title'})
        #print h2content
        if h2content is not None:
            link=h2content.find('a')
            mylink=link.get('href')
            quectionlink='http://www.zhihu.com'+mylink
            enterquestionpage(quectionlink)
            print quectionlink         




postdatastr=urllib.urlencode(postdata)

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
urllib2.install_opener(opener)

h = urllib2.urlopen(loginurl) 
request = urllib2.Request(loginurl,postdatastr,headers)
response = urllib2.urlopen(request)
text = response.read()

collecturl='http://www.zhihu.com/collections'
txt=urllib2.urlopen(collecturl).read()
file=open('123.html','w')
file.write(txt)

soup=BeautifulSoup(txt)
count=0
for div in soup.findAll('div',{'class':'zm-item'}):
    link=div.find('a')
    mylink=link.get('href')
    collectlink='http://www.zhihu.com'+mylink
    entercollectpage(collectlink)
    print collectlink
    count+=1
mydoc.save('123.docx')
    #    exit(1)
        
print 'the end'
