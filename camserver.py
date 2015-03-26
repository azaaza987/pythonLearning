from VideoCapture import Device
import ImageDraw, sys, pygame, time
from pygame.locals import *
import socket
import time
from PIL import ImageEnhance
from threading import Thread
import traceback
import threading




# ȫ�ֱ���
is_sending = False
cli_address = ('', 0)

# ������ַ�Ͷ˿�
host = 'localhost'
port = 10218

# ��ʼ��UDP socket
ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind((host, port))

# �����߳��࣬���ڽ��տͻ��˷��͵���Ϣ
class UdpReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
                
    def run(self):
        while not self.thread_stop:
            # ����ȫ�ֱ�����������Ϣ�����
            global cli_address   
            global is_sending
            try:
                message, address = ser_socket.recvfrom(2048)
            except:
                traceback.print_exc()
                continue
            print message,cli_address
            cli_address = address
            if message == 'startCam':
                print 'start camera',
                is_sending = True
                ser_socket.sendto('startRcv', cli_address)                
            if message == 'quitCam':
                is_sending = False
                print 'quit camera',

    def stop(self):
        self.thread_stop = True

# ���������߳�


    
def disp(phrase,loc):
    s = font.render(phrase, True, (200,200,200))
    sh = font.render(phrase, True, (50,50,50))
    screen.blit(sh, (loc[0]+1,loc[1]+1))
    screen.blit(s, loc)

if __name__=='__main__':
    res = (640,480)
   
    cam = Device()
    cam.setResolution(res[0],res[1])
 
    
    brightness = 1.0
    contrast = 1.0
    shots = 0
    
    receiveThread = UdpReceiver()
    receiveThread.setDaemon(True)           # ��ѡ�����ú�ʹ�����߳��˳������߳�ͬʱ�˳�
    receiveThread.start()
    

    while 1:
        if is_sending: 
            camshot = ImageEnhance.Brightness(cam.getImage()).enhance(brightness)
            camshot = ImageEnhance.Contrast(camshot).enhance(contrast)
            clock = pygame.time.Clock()
            img = cam.getImage().resize((160,120))
            data = img.tostring()
            ser_socket.sendto(data, cli_address) 
            time.sleep(0.05) 
        else:
            time.sleep(1)
    receiveThread.stop()
    ser_socket.close()        