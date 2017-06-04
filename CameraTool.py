#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: Apache Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: CameraTool.py
@time: 16/9/20 下午7:45
"""

import datetime
import cv2
import numpy

#import librtmp
rtmpurl = 'rtmp://192.168.33.11:1935/hls/mystream'


# ffmpeg -f avfoundation -framerate 30   -i "0" \-c:v libx264 -preset ultrafast -acodec libmp3lame -ar 44100 -ac 1  -f flv rtmp://192.168.33.11:1935/hls/mystream




class OpenCVHelper():
    def __init__(self, cascPath=None, isShowFace=True):
        if not cascPath:
            cascPath = '/usr/local/Cellar/opencv/HEAD-9ff63a4_3/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
        #创建级联
        #级联就是一个包含了用于人脸检测的数据的XML文件。
        self.faceCascade = cv2.CascadeClassifier(cascPath)
        self.cap = cap = cv2.VideoCapture(0)
        self.isShowFace = isShowFace

    def GetFaces(self, frame):
        return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #读取图片并进行灰度转换。在进行灰度转换过程中已经完成了OpenCV的多个操作步骤。
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            #flags=cv2.CV_HAAR_SCALE_IMAGE
        )
        # print faces
        return faces

    def Run(self):
        while (1):
            ##读取摄像头
            retval, frame = self.cap.read()
            if (self.isShowFace):
                faces = self.GetFaces(frame)
                print faces
                if faces and len(faces):
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #显示
            cv2.imshow('video', frame)
            key = cv2.waitKey(10)
            if key == ord('s'):  # 当按下"s"键时，将保存当前画面
                cv2.imwrite('screenshot.bmp', frame)
            elif key == ord('q'):  # 当按下"q"键时，将退出循环
                break


class RTMPClient():
    def __init__(self):
        self.rtmpurl=rtmpurl
    def GetDate(self):
        client=librtmp.RTMP(rtmpurl)
        client.connect(None)
        stream=client.create_stream(0,True)
        print stream


if __name__ == '__main__':
    helper = OpenCVHelper()
    helper.Run()
    #pass
    #client=RTMPClient()
    #client.GetDate()

"""
def getFace(frame):
    img = cv2.imread(frame)

    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img  # if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

    faces = faceCascade.detectMultiScale(gray, 1.2, 5)  # 1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    result = []
    for (x, y, width, height) in faces:
        result.append((x, y, x + width, y + height))
    return result
"""

"""

while(1):
    retval, frame = cap.read()

    key = cv2.waitKey(10)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(

        gray,

        scaleFactor=1.1,

        minNeighbors=5,

        minSize=(30, 30),

        flags=cv2.cv.CV_HAAR_SCALE_IMAGE

    )
    print faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    cv2.imshow('video', frame)
    if key == ord('s'):  # 当按下"s"键时，将保存当前画面
        cv2.imwrite('screenshot.bmp', frame)
    elif key == ord('q'):  # 当按下"q"键时，将退出循环
        break

#cap.release()
#cv2.destroyAllWindows()
"""
