# -*- coding: utf-8 -*-
import cv2
import numpy as np

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingData.yml")
id_ = 0
font = cv2.FONT_HERSHEY_SIMPLEX
labels = {1:"Onur", 2: "<>", 3: "<>", -1: "Bilinmeyen"}
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5)
    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        id_, conf = recognizer.predict(gray[y: y + h, x: x + w])
        if(conf < 40):
            print(id_, conf)
        else:
            id_ = -1
        color = (0, 0, 255)
        stroke = 2
        cv2.putText(frame, labels[id_], (x, y + h), font, 1, color, stroke, cv2.LINE_AA)
    cv2.imshow("frame", frame)
    if(cv2.waitKey(1) == ord("q")):
        break
        
cap.release()
cv2.destroyAllWindows()

