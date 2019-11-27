# -*- coding: utf-8 -*-
import cv2
import imutils

video_capture = cv2.VideoCapture(0)
frame = video_capture.read()[1]

def motion_detection():
    print("Başladım")
    video_capture = cv2.VideoCapture(0)
    first_frame = None
    
    while True:
        """2 tane output verir retval, frame [1] framei seçer."""
        frame = video_capture.read()[1]
        
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
        
        thresh = cv2.threshold(frame_delta, 125, 255, cv2.THRESH_BINARY)[1] # 125 değerinin üzerindeki her pikseli beyaza dönüştür.
        
        dilate_image = cv2.dilate(thresh, None, iterations = 2) # siyah beyaz karedeki beyazlara 2 kez genişletme işlemi yap.
        
        cnt = cv2.findContours(dilate_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # karedeki beyazların konumunu verir.
        
        for c in cnt:
            if cv2.contourArea(c) > 700: # beyazlı bölgenin alanı 700'den büyükse... (Ortam parlaklığına göre değiştirilmelidir.)
                cv2.destroyAllWindows()
                return "motion"
                break
            else:
                pass
        

