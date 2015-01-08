#python爬虫抓取网站图片并保存
import urllib2
from bs4 import BeautifulSoup
import socket
 
baseurl = "http://dbmeizi.com/"
#伪装浏览器,以免被封
def user_agent(url):
    req_header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req_timeout = 20
    try:
        req = urllib2.Request(url,None,req_header)
        page = urllib2.urlopen(req,None,req_timeout)
        html = page
    except urllib2.URLError as e:
        print e.message
    except socket.timeout as e:
        user_agent(url)
    return html
 
def page_loop(pageid):
    url = baseurl+'?p=%s'%pageid
    print url
    page = user_agent(url)
    soup = BeautifulSoup(page)
    total_img = 0
    img = soup.find_all(['img'])
    for myimg in img:
        link = myimg.get('src')
        total_img += 1
        print link
      #  content2 = urllib2.urlopen(link).read()
        content2 = user_agent(link).read()
        #这句代码直接从OSC上面弄下来的
        #D:\myimg是保存路径,你可以自己改成自己的,但是路径必须要自己创建好
        with open(u'D:\myimg'+'/'+link[-11:],'wb') as code:
            code.write(content2)
    print total_img
    return total_img
page_start = 0
page_stop = 4
total = 0
for i in range(page_start,page_stop):
    total+=page_loop(i)
 
print total
#total就是统计下总共保存到本地的图片数量