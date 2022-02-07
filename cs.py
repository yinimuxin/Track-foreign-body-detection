# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import time
import datetime

cap = cv2.VideoCapture(0)

avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
time.sleep(10)
while(True):
    # 逐帧获取图像
    tiestamp = datetime.datetime.now()
    ret, frame = cap.read()
    text = "unoccupied"
    if not ret:
        break


    # 对每帧图像进行操作
    gray = cv2.resize(frame,width=500)#调整大小
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#变成灰色图像
    gray = cv2.GaussianBlur(gray,(21,21),0)#高斯滤波
    if avg is None:
        avg = gray.copy().astype("float")
        continue
    cv2.accumulateWeighted(gray,avg,0.5)
    # 显示处理后的图像
    cv2.imshow('frame',gray)
    #计算当前帧与第一帧的区别
    frameDelta = cv2.absdiff(gray,cv2.convertScaleAbs(avg))
   # cv2.imshow('first2',frameDelta)
   #填充孔洞
    thresh = cv2.threshold(frameDelta, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cv2.imshow('thresh',thresh)
    #查找轮廓
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
  #  cv2.imshow('thresh2',thresh.copy())
    for c in contours:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 500:
           continue

        # 计算轮廓的边界框，在当前帧中画出该框
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('found',frame)
        text = "Occupied"
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    #if text == "Occupied":
      #  if (timestamp-lastUploaded).second>=2:
           # motionCounter+=1
            #if motionCounter>=23:


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
if cv2.waitKey(1) & 0xFF == ord('q'):
# break When everything done, release the capture
cap.release()
cv2.destroyAllWindows()