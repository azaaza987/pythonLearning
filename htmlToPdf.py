# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from xhtml2pdf import pisa
import chardet
import urllib2
import pdfkit




urls=['http://www.cnblogs.com/leslies2/archive/2012/07/30/2608784.html',
      'http://www.cnblogs.com/leslies2/archive/2012/03/22/2389318.html',
      'http://www.cnblogs.com/leslies2/p/3727762.html',
      'http://www.cnblogs.com/leslies2/archive/2012/02/07/2310495.html',
      'http://www.cnblogs.com/leslies2/archive/2012/02/08/2320914.html',
      'http://www.cnblogs.com/leslies2/archive/2012/03/06/2379235.html',
      'http://www.cnblogs.com/leslies2/archive/2012/01/05/2289106.html'
      ]


def useragent(url):
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
                 "Referer": 'http://baidu.com/'}

    req = urllib2.Request(url, headers=i_headers)
    html = urllib2.urlopen(req).read()
    return html


def gethtml(url):
    html = useragent(url)
    soup = BeautifulSoup(html,"lxml")
    div = soup.find("div", {"class": "post"})
    return str(div)


def SaveHtml(html, outputfile):


    resultFile = open(outputfile, "w+b")
    pisaStatus = pisa.CreatePDF(html,dest=resultFile)
    resultFile.close()
    return pisaStatus.err


if __name__ == '__main__':
    html="""<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>"""

    for url in urls:
        html+=gethtml(url)

    file=open(r'd:/123.html','w')
    file.writelines(html)
    file.close()

    #html=u''.join(html)
    #SaveHtml(html,r'd:/1234.pdf')
    #pdfkit.from_string(html,r'd:/1234.pdf')
    pdfkit.from_file(r'd:/123.html',r'd:/1234.pdf')


