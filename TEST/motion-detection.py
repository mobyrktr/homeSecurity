# -*- coding: utf-8 -*-
import cv2
import time
import datetime
import imutils

def motion_detection():
    video_capture = cv2.VideoCapture(0)
    time.sleep(2)
    first_frame = None
    
    while True:
        """2 tane output verir retval, frame [1] framei seçer."""
        frame = video_capture.read()[1]
        text = "Tespit Edilmedi"
        
        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Kareleri griye dönüştürür.
        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21, 21), 0) # 21x21'lik bir çekirdek ile griölçekli kareyi dolaş ve bulanıklaştır.
        blur_frame = cv2.blur(gaussian_frame, (5, 5)) # 5x5'lik bir çekirdek ile tekrar bulanıklaştır.
        greyscale_image = blur_frame
        if first_frame is None:
            first_frame = greyscale_image
        else:
            pass
        
        frame = imutils.resize(frame, width = 500)
        frame_delta = cv2.absdiff(first_frame, greyscale_image) # Hareketi gözlemlemek için iki kare arasındaki piksel farklarını bulur.
        
        thresh = cv2.threshold(frame_delta, 60, 255, cv2.THRESH_BINARY)[1] # 125 değerinin üzerindeki her pikseli beyaza dönüştür.
        
        dilate_image = cv2.dilate(thresh, None, iterations = 2) # siyah beyaz karedeki beyazlara 2 kez genişletme işlemi yap.
        
        cnt = cv2.findContours(dilate_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # karedeki beyazların konumunu verir.
        
        for c in cnt:
            if cv2.contourArea(c) > 3000: # beyazlı bölgenin alanı 700'den büyükse...
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = 'Tespit Edildi'
            else:
                pass
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        cv2.putText(frame, f'[+] Hareket: {text}', (10, 20), font, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'), 
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX , 0.35, (0, 0, 255),1)
        cv2.imshow('Security Feed', frame)
        cv2.imshow('Threshold(foreground mask)', dilate_image)
        cv2.imshow('Frame_delta', frame_delta)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

motion_detection()
            

