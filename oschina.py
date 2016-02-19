# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import urllib2

import datetime
import PyRSS2Gen
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')




class OSCRssSpider():
    def __init__(self):
        self.myrss = PyRSS2Gen.RSS2(title='OSChina',
                                    link='http://my.oschina.net',
                                    description=str(datetime.date.today()),
                                    items=[]
                                    )
        self.baseurl="http://www.oschina.net/blog"

    def useragent(self,url):
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", \
    "Referer": 'http://baidu.com/'}
        req = urllib2.Request(url, headers=i_headers)
        html = urllib2.urlopen(req).read()
        return html
    def enterpage(self,url):
        pattern = re.compile(r'\d{4}\S\d{2}\S\d{2}\s\d{2}\S\d{2}')
        rsp=self.useragent(url)
        soup=BeautifulSoup(rsp)
        timespan=soup.find('div',{'class':'BlogStat'})
        timespan=str(timespan).strip().replace('\n','').decode('utf-8')
        match=re.search(r'\d{4}\S\d{2}\S\d{2}\s\d{2}\S\d{2}',timespan)
        timestr=str(datetime.date.today())
        if match:
            timestr=match.group()
            #print timestr
        ititle=soup.title.string
        div=soup.find('div',{'class':'BlogContent'})
        rss=PyRSS2Gen.RSSItem(
                              title=ititle,
                              link=url,
                              description = str(div),
                              pubDate = timestr
                              )
    
        return rss
    def getcontent(self):
        rsp=self.useragent(self.baseurl)
        soup=BeautifulSoup(rsp)
        ul=soup.find('div',{'id':'RecentBlogs'})
        for li in ul.findAll('li'):
            div=li.find('div')
            if div is not None:
                alink=div.find('a')
                if alink is not None:
                    link=alink.get('href')
                    print link
                    html=self.enterpage(link)
                    self.myrss.items.append(html)
    def SaveRssFile(self,filename):
        finallxml=self.myrss.to_xml(encoding='utf-8')
        file=open(filename,'w')
        file.writelines(finallxml)
        file.close()
        


if __name__=='__main__':
    rssSpider=OSCRssSpider()
    rssSpider.getcontent()
    rssSpider.SaveRssFile('oschina.xml')
