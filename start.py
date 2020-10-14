# -*- coding: utf-8 -*-
import motionDetection as m
import faceDetector as f
from collections import Counter
import TTS as t
#import serial # arduino ile haberleşme için (Daha sonra kullanılacak.)
import cv2

#arduino = serial.Serial("COM8", 115200, timeout = 1) arduino haberleşmesini başlatmak için
alarmCal = False
tara = m.motion_detection()
print("motion detection: ", tara)
if tara == "motion": # hareket algılanırsa...
    while True:
        cap = cv2.VideoCapture()
        frame = cap.read()[1]
        #print(alarmCal)
        if(alarmCal): # arduino'ya serial üzerinden veri göndererek alarmı çalıştıracak.
            pass # Daha sonra doldurulacak.
        face = f.Recognize() # yüzü 20 kere tahmin edecek ve her tahminini listeye ekleyecek.
        counter = Counter(face) # tahminlerin arasında en çok tekrar edeni doğru yüz olarak kabul edecek.
        tekrar = counter.most_common(1)
        kisi = tekrar[0][0]
        print(kisi)
        if(kisi == -1): # kişi sistemde ekli değilse id'si -1'dir.
            alarmCal = True
        else:
            alarmCal = False
            t.hosgeldin(kisi) # Hoşgeldin <kisiadi> şeklinde ses verilecek.
            cap.release()
            cv2.destroyAllWindows()
            break
            
    
    
    
    
    


