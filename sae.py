#ʹ��sae��storage�������Զ��������ݿ��ļ�
import sae
from sae.storage import Bucket
import urllib2
import smtplib
import time
from email.message import Message
import email.utils
import base64
 
 
correct_time = time.strftime('%m_%d_%H_%M_%S',time.localtime(time.time()))
url = "xxxxxxxxxxxxx"����޸ĳ�������ݿ��ļ��ĵ�ַ
 
def send_email(file_url):
    smtpserver = 'smtp.gmail.com'
    #�����Ҷ��ܿ�����,�޸ĳ����Լ���.
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
    bucket = Bucket('sssssss') #�޸ĳ����Լ���storage��
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