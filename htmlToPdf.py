# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from xhtml2pdf import pisa
import chardet
import urllib2
import pdfkit

baseurl = 'http://www.cnblogs.com/plin2008/archive/2009/05/05/1450201.html'


def useragent(url):
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
                 "Referer": 'http://baidu.com/'}

    req = urllib2.Request(url, headers=i_headers)
    html = urllib2.urlopen(req).read()
    return html


def gethtml():
    html = useragent(baseurl)
    soup = BeautifulSoup(html,"lxml")
    div = soup.find("div", {"class": "post"})
    return str(div)


def SaveHtml(html, outputfile):


    resultFile = open(outputfile, "w+b")
    pisaStatus = pisa.CreatePDF(html,dest=resultFile)
    resultFile.close()
    return pisaStatus.err


if __name__ == '__main__':
    html=gethtml()
    html="""<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>"""+html
    file=open(r'd:/123.html','w')
    file.writelines(html)
    file.close()

    #html=u''.join(html)

    #pdfkit.from_string(html,r'd:/1234.pdf')
    pdfkit.from_file(r'd:/123.html',r'd:/1234.pdf')


