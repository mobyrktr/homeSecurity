# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sqlite3
from collections import Counter
from time import time

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") # Karede yüz olup olmadığını görmemizi sağlayan dosya


def Recognize(tahmin = 60, decision_time = 10):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer/trainingData.yml") # Yüzleri tanımak için oluşturduğumuz dosyayı okuduk
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    id_ = 0
    labels = dict()
    cursor = connection.execute("select id, f_name from users")
    for row in cursor:
        labels[int(row[0])] = row[1]
        
    connection.close()
    yuz = list()
    cap = cv2.VideoCapture(0) # Varsayılan kayıt cihazını seçtik
    end_time = time() + decision_time 

    while len(yuz) <= 20 and time() <= end_time:
        frame = cap.read()[1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Kareyi griye çevirme işlemi
        faces = cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5) # karedeki yüzleri buldurduk
        for(x, y, w, h) in faces: # x, y --> başlangıç noktaları, w --> genişlik, h --> yükseklik
            id_, conf = recognizer.predict(gray[y: y + h, x: x + w]) # id_ --> yüz id, conf --> tahminin doğruluğu(ne kadar düşük o kadar doğru)
            if conf < tahmin: # Bu değer ortama göre değişiklik gösterir.
                yuz.append(labels[id_]) # conf değeri 45'in altındaysa doğru tahmin yaptığını varsayıyoruz.
            else:
                yuz.append(-1) # conf değeri 45'in üstündeyse kişi sistemde kayıtlı değilmiş gibi işlem yapıyoruz.
    if len(yuz) == 0:
        return -1, 0

    counter = Counter(yuz) # tahminlerin arasında en çok tekrar edeni doğru yüz olarak kabul edecek.
    tekrar = counter.most_common(1)
    kisi = tekrar[0][0]
    
    cap.release()
    cv2.destroyAllWindows()
    return kisi, conf