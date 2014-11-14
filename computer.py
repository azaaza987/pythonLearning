##远程控制电脑并关机
##博客地址:http://www.lylinux.org/python%E8%BF%9C%E7%A8%8B%E7%9B%91%E6%8E%A7%E7%94%B5%E8%84%91%E5%B9%B6%E5%85%B3%E6%9C%BA.html
import time
from VideoCapture import Device
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib
from PIL import ImageGrab
from PIL import ImageEnhance
import os
from fetion import *
import poplib,email



def get_correcttime() :
    open_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
    return open_time


def get_desktopimg(correcttime):
    filename = r"F:/learn/watchcomputer/desktop" + correcttime + ".jpg"
    pic = ImageGrab.grab()
    pic.save(filename)
    print "desktop img saved ok!!!!"
    return filename
   


def get_webcamimg(correcttime):
    filename = r"F:/learn/watchcomputer/webcam" + correcttime + ".jpg"
    cam = Device()
    
    res = (640,480)
    cam = Device()
    cam.setResolution(res[0],res[1])
    
    brightness = 1.0
    contrast = 1.0
    
    camshot = ImageEnhance.Brightness(cam.getImage()).enhance(brightness)
    camshot = ImageEnhance.Contrast(camshot).enhance(contrast)
    time.sleep(10)
    cam.saveSnapshot(filename,timestamp=3, boldfont=1, quality=80)
    print "webcam img saved ok!!!!!!"
    return filename

def send_img(desktop,webcam):
    try:
        from_mail = "ddddddddd@gmail.com"
        to_mail = "fffffffffffff@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = from_mail
        msg['To'] = to_mail
        msg['Subject'] = 'my computer'
        body = 'test img send'
        html_code = '<b><i>the guy who use my computer and the screen shot.</b></i> <img alt="desktop" src="cid:image1" width="683" height="384"/><img alt="webcam" src="cid:image2"/>'
        print html_code
        con = MIMEText(html_code,'html','utf-8')
        msg.attach(con)
        img1 = MIMEImage(file(desktop,'rb').read())
        img2 = MIMEImage(file(webcam,'rb').read())
        img1.add_header('Content-ID','<image1>')
        img2.add_header('Content-ID','<image2>')
        msg.attach(img1)
        msg.attach(img2)
        server = smtplib.SMTP('smtp.gmail.com')
        server.docmd('ehol',from_mail)
        server.starttls()
        server.login(from_mail,'wwwwwwwwwwwwwwwwwwwwwwwwww')
        server.sendmail(from_mail,to_mail,msg.as_string())
        server.quit()
        print "mail send ok!!!!!"
        return True        
    except:
        return False


def write_log(issuccess,smsissend):
    log_file_dir = r"F:/learn/watchcomputer/computer.log"
    log_flie = file(log_file_dir,'a')
    log_flie.write('at '+now_time + '  img saved success! ')
    if (issuccess):
        log_flie.write('mail send success!!!')
    elif(not issuccess):
        log_flie.write('mail send failed!!!')
    if (smsIsSend):
        log_flie.write('sms send success')
    elif(not smsIsSend):
        log_flie.write('sms send failed')
    log_flie.write('\n\n')
    log_flie.close()



def send_sms(correct_time):
    myphone = '11111111'
    mypwd = '2222222222222'
    tophone = '33333333333333333'
    
   
    print 'send to '+tophone
    sms = 'computer is open at '+correct_time
    try:
        fetion = PyFetion(myphone,mypwd,'TCP')
        fetion.login(FetionHidden)        
        fetion.send_sms(sms,tophone,True)
        fetion.logout()
        return True
    except:
        return False




def accpmail():
    try:
        p=poplib.POP3_SSL('pop.gmail.com')
        p.user("recent:wwwwwwwwwwwwwwwww@gmail.com")
        p.pass_('ffffffffffffffffffffffff')
        
        ret = p.stat()
    except poplib.error_proto,e:
        print "Login failed:",e
        return "fail"
    print "Login succeeded"
    mailnum=ret[0]
    down=p.retr(mailnum)
    for i in down[1]:
        if i.find("Subject:")==0:
            cmdstr=i
            print cmdstr
            break
    p.quit()
    return cmdstr


time.sleep(240)    
now_time = get_correcttime()
desktopimg = get_desktopimg(now_time)
webcamimg  = get_webcamimg(now_time)

smsIsSend = send_sms(now_time)


if(os.path.isfile(desktopimg) and os.path.isfile(webcamimg)): 
    MailIsSend = send_img(desktopimg,webcamimg)
    write_log(MailIsSend,smsIsSend)

while True:
    cmdstr = accpmail()
    if cmdstr != "fail":
        if cmdstr.find('shutdown')!=-1:
            os.system("123.mp3")
        elif cmdstr.find("quit") != -1:
            break
        elif cmdstr.find("continue") != -1:
            time.sleep(120)
            continue
    else:
        time.sleep(120)
        continue


