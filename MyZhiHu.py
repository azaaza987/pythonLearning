#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liangliang'

from bs4 import BeautifulSoup
import  urllib2
import  urllib
import cookielib
import re

from ebooklib import epub


headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
    'Host':'www.zhihu.com',
    'Origin':'http://www.zhihu.com',
    'Connection':'keep-alive',
    'CSP':'active',
    'X-Requested-With':'XMLHttpRequest',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Referer':'http://www.zhihu.com/people/zihaolucky/followers',
    'Content-Type':'application/x-www-form-urlencoded',
    }

postdata={
  '_xsrf':  '23cc1f7872b34128755d9aeed4e22789',
  'email':  'liangliangyy@gmail.com',
  'password': 'xxxxxxx',
  'rememberme':'y'
}

loginurl='http://www.zhihu.com/login'

class MyZhiHu():
    def __init__(self):
        xsrf=self.__getxsrf()

        postdata['_xsrf']=xsrf
        self.headers=headers
        self.postdatastr=urllib.urlencode(postdata)
        self.loginurl=loginurl
        self.cj = cookielib.LWPCookieJar()
        self.book = epub.EpubBook()
        # set metadata
        # book.set_identifier('id123456')
        self.book.set_title('Sample book')
        self.book.set_language('cn')

        self.book.add_author('Author Authorowski')
        self.book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')


    def __getxsrf(self):

        requrl='http://www.zhihu.com/#signin'
        html=urllib2.urlopen(requrl).read()
        reg = r'name="_xsrf" value="(.*)"/>'
        pattern = re.compile(reg)
        result = pattern.findall(html)
        xsrf = result[0]
        return  xsrf

    def __getcheckcode(self,thehtml):
        soup=BeautifulSoup(thehtml)
        div=soup.find('div',{'class':'js-captcha captcha-wrap'})
        if div is not None:
            imgsrc=div.find('img')
            imglink=imgsrc.get('src')
            if imglink is not None:
                imglink='http://www.zhihu.com'+imglink
                imgcontent=urllib2.urlopen(imglink).read()
                with open('checkcode.gif','wb') as code:
                    code.write(imgcontent)
                return True
            else:
                return False
        return False




    def __loginzhihu(self):

        cookie_support = urllib2.HTTPCookieProcessor(self.cj)
        opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        #h = urllib2.urlopen(loginurl)
        request = urllib2.Request(loginurl,self.postdatastr,self.headers)
        response = urllib2.urlopen(request)
        txt = response.read()
        if self.__getcheckcode(txt):
            checkcode=raw_input('input checkcode:')
            self.postdata['captcha']=checkcode
            self.__loginzhihu()
        else:
            #self.__loginzhihu()
            print('login ok')

    def __useragent(self,url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
    "Referer": 'http://baidu.com/'}
        req = urllib2.Request(url, headers=i_headers)
        html = urllib2.urlopen(req).read()
        return html

    def login(self):

        self.__loginzhihu()

    def EnterQuestion(self,url):
        html=self.__useragent(url)
        soup=BeautifulSoup(html)
        questiontitle=soup.title.string
        print(questiontitle)
        i=0
        for div in soup.findAll('div',{'class':' zm-editable-content clearfix'}):
            i+=1
            filename='chap_'+str(i)+'.xhtml'
            print(filename)
            c1 = epub.EpubHtml(title=filename, file_name=filename, lang='zh')
            c1.content=div
            self.book.add_item(c1)
            self.book.toc = (epub.Link(filename, filename, 'intro'),
             (epub.Section('Simple book'),
             (c1, ))
            )

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        self.book.spine = ['nav', c1]


    def GetCollection(self):
        html=self.__useragent('http://www.zhihu.com/collections')
        soup=BeautifulSoup(html)
        print(soup.title.string)
        self.EnterQuestion('http://www.zhihu.com/question/28636966')
        epub.write_epub('test1.epub', self.book, {})