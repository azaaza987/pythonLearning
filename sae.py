# -*- coding: UTF-8 -*-

#使用sae的storage服务来自动保存数据库文件
import sae
from sae.storage import Bucket
import urllib2
import smtplib
import time
from email.message import Message
import email.utils
import base64
 
 
correct_time = time.strftime('%m_%d_%H_%M_%S',time.localtime(time.time()))
url = "xxxxxxxxxxxxx" #这个修改成你的数据库文件的地址
 
def send_email(file_url):
    smtpserver = 'smtp.gmail.com'
    #这儿大家都能看懂吧,修改成你自己的.
    username = 'ooooooo'
    password = 'xxxxxxxxxx'
    from_addr = 'ffffffff@gmail.com'
    to_addr = 'tttttttt@gmail.com'
    message = Message()
    message['Subject'] = 'Sql Data Backup'
    message['From'] = from_addr
    message['To'] = to_addr
    message.set_payload('Sql Data Backup OK at '+correct_time + ' url is  '+file_url)
    msg = message.as_string()
    sm = smtplib.SMTP(smtpserver,port=587,timeout=20)
    sm.ehlo()
    sm.starttls()
    sm.ehlo()
    sm.login(username, password)
    sm.sendmail(from_addr, to_addr, msg)
    sm.quit() 
 
def checktest():
    bucket = Bucket('sssssss')  #修改成你自己的storage名s
    bucket.put()
    bucket.post(acl='.r:.sinaapp.com,.r:sae.sina.com.cn', metadata={'expires': '1d'})
    f = urllib2.urlopen(url)
    data = f.read()
    bucket.put_object(correct_time+".sql", data)
    file_url = bucket.generate_url(correct_time+".sql")
    return file_url
def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)
    file_url = checktest()
    send_email(file_url)
     
    return ['<strong>Welcome to SAE!</strong>']
 
 
application = sae.create_wsgi_app(app)