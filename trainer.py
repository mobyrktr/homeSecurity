# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = "dataSet"

def getImagesWithID(path):
    imagePaths = list()
    for f in os.listdir(path): # klasör altındaki bütün dosyaları içeren liste --> User.2.1.jpg
        imagePaths.append(os.path.join(path, f)) # dosya yolu ile dosya adını birleştirdik --> dataSet\\User.2.1.jpg
    faces = list()
    IDs = list()
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath)
        faceArray = np.array(faceImg, "uint8") # listeyi numpy dizisine çevirdik.
        ID = int(os.path.split(imagePath)[-1].split(".")[1]) # dosya adından id'yi aldık.
        faces.append(faceArray)
        IDs.append(ID)
        cv2.imshow("training", faceArray)
        cv2.waitKey(10)
    return np.array(IDs), faces

def train():
    IDs, faces = getImagesWithID(path)
    recognizer.train(faces, IDs)
    recognizer.save("recognizer/trainingData.yml")
    cv2.destroyAllWindows()


