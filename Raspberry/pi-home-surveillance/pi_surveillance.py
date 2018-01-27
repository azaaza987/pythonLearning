import datetime
import time
import cv2
import logging
import imutils
import os

lastSaveTime = datetime.datetime.now()
motionCounter = 0
path = os.path.split(os.path.realpath(__file__))[0]
avg = None
cap = None
logfilename = path + '/logger.log'
logging.basicConfig(filename=logfilename, level=logging.INFO)
while (1):

    timestamp = datetime.datetime.now()
    if timestamp.hour >= 18 or timestamp.hour <= 9:
        logging.info('time:' + str(timestamp.hour))
        time.sleep(10)
        continue
    text = "Unoccupied"
    if cap is None:
        cap = cv2.VideoCapture(0)
    # 从摄像头逐帧捕获数据
    ret, frame = cap.read()
    # 调整帧尺寸，转换为灰阶图像并进行模糊
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # 如果平均帧是None，初始化它
    if avg is None:
        logging.info("[INFO] starting background model...")
        avg = gray.copy().astype("float")
        continue
    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between the current
    # frame and running average
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # 对变化图像进行阀值化, 膨胀阀值图像来填补
    # 孔洞, 在阀值图像上找到轮廓线
    thresh = cv2.threshold(frameDelta, 5, 255,
                           cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    s = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                         cv2.CHAIN_APPROX_SIMPLE)

    _, cnts, hierarchy = s

    # 遍历轮廓线
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 6000:
            continue

        # 计算轮廓线的外框, 在当前帧上画出外框,
        # 并且更新文本

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"



    if text == "Occupied":
        if (timestamp - lastSaveTime).seconds >= 3:
            # increment the motion counter
            motionCounter += 1
            # 判断包含连续运动的帧数是否已经
            # 足够多
            if motionCounter >= 3:
                # 在当前帧上标记文本和时间戳
                ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
                cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.35, (0, 0, 255), 1)
                filename = path + '/imgs/img_' + ts + '.jpg'
                lastSaveTime = timestamp
                motionCounter = 0
                cv2.imwrite(filename, frame)
                # 显示图像
                # cv2.imshow("capture", frame)
                logging.info('Occupied:' + ts)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    else:
        motionCounter = 0
