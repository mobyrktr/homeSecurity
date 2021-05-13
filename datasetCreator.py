# -*- coding: utf-8 -*-
import cv2
import numpy as np

def createDataSet(id_):
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    counter = 0
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            counter += 1
            cv2.imwrite("dataSet/User." + str(id_) + "." + str(counter) + ".jpg", gray[y: y + h, x: x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.waitKey(100)
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
        if(counter > 20):
            cap.release()
            cv2.destroyAllWindows()
            break
            
                 
