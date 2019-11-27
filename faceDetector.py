# -*- coding: utf-8 -*-
import cv2
import numpy as np

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") # Karede yüz olup olmadığını görmemizi sağlayan dosya
cap = cv2.VideoCapture(0) # Varsayılan kayıt cihazını seçtik
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingData.yml") # Yüzleri tanımak için oluşturduğumuz dosyayı okuduk
    

def Recognize():
    id_ = 0
    labels = {1:"<isim1>", 2: "<isim2>"} 
    yuz = []
    while len(yuz) <= 20:
        frame = cap.read()[1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Kareyi griye çevirme işlemi
        faces = cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5) # karedeki yüzleri buldurduk
        for(x, y, w, h) in faces: # x, y --> başlangıç noktaları, w --> genişlik, h --> yükseklik
            id_, conf = recognizer.predict(gray[y: y + h, x: x + w]) # id_ --> yüz id, conf --> tahminin doğruluğu(ne kadar düşük o kadar doğru)
            if conf < 45: # Bu değer ortama göre değişiklik gösterir.
                yuz.append(labels[id_]) # conf değeri 45'in altındaysa doğru tahmin yaptığını varsayıyoruz.
            else:
                yuz.append(-1) # conf değeri 45'in üstündeyse kişi sistemde kayıtlı değilmiş gibi işlem yapıyoruz.
    return yuz