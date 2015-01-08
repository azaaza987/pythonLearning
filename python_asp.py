#pythonµÇÂ½aspÍøÕ¾Ò³Ãæ
#blog http://www.lylinux.org/python%E7%99%BB%E9%99%86asp%E9%A1%B5%E9%9D%A2.html
#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import urllib
import cookielib
import re
import httplib
import time
 
 
loginUrl="µÇÂ¼µØÖ·"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"}
studentCookie = cookielib.CookieJar() 
pageOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(studentCookie))
loginPageRequest = urllib2.Request(loginUrl) 
loginPageHTML = pageOpener.open(loginPageRequest).read()
"""
s=requests.Session()
s.headers.update(headers)
r=s.get(loginUrl)
"""
print loginPageHTML
soup=BeautifulSoup(loginPageHTML)
 
__VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
__EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")['value']
 
print __VIEWSTATE
print __EVENTVALIDATION
 
login_data={
     ' __EVENTTARGET':'',
'__EVENTARGUMENT':'',
'__LASTFOCUS':'',
'__VIEWSTATE':__VIEWSTATE,
'__EVENTVALIDATION':__EVENTVALIDATION,
'ClienScreentHeight':'768',
'TextBoxUserID':'username',
'TextBoxPWD':'password',
'drpLanguage':'zh-CN',
'ButtonConfirm.x':'45',
'ButtonConfirm.y':'64'
      }
loginHeader = { 
                    
                    'User-Agent':'sssssssssssssssssssssss' 
                    }
loginData=urllib.urlencode(login_data)
loginRequest = urllib2.Request(loginUrl , loginData , headers)
loginResponse = pageOpener.open(loginRequest)
 
print loginResponse
 
theurl='µÇÂ¼ºóËÑË÷Ò³ÃæµØÖ·'
 
mainPageRequest = urllib2.Request(theurl)
 
mainPageHTML = pageOpener.open(mainPageRequest).read() 
soup=BeautifulSoup(mainPageHTML)
 
__VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
#__EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")['value']
 
print __VIEWSTATE
#print __EVENTVALIDATION
 
searchdata={
            '__VIEWSTATE':__VIEWSTATE,
            '__EVENTVALIDATION':'',
            'txtCopNO':'',
'txtCAR_NO_S':'',
'drpStatus':'',
'txtHiddenOrOnline':'none',
'txtAuto_id':'',
'drpType':'',
'drpBaseType':'',
'ddlIsStatus':0,
'txtICCard':'',
'txtBILL_NO':'',
'txtGDateTime1':'',
'txtGDateTime2':'',
'drpFromKA':'',
'drpToKA':'',
'btnSearch':'%E6%9F%A5+%E8%AF%A2%28F%29'
}
 
data2=urllib.urlencode(searchdata)
 
 
  
 
searchData=urllib.urlencode(searchdata)
searcgRequest=urllib2.Request(theurl , searchData , headers)
searchResponse=pageOpener.open(searcgRequest)
 
print loginResponse
print searchResponse
 
searchHtml=searchResponse.read()
 
 
filename= r'C:\Users\Dell\Desktop\getlogin\file'+time.strftime('%d%H%M',time.localtime(time.time()))+'.html'
 
file=open(filename,'w')
file.write(searchHtml)
file.close()
 
print 'end'