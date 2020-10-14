# -*- coding: utf-8 -*-
import sqlite3
import datasetCreator as dsc
import os
import trainer as tr
import TTS as tts
import time
import serial

#add user
def kullaniciEkle(ad, soyad, kart_uid, adminMi, username = None, password = None, e_mail = None):
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    connection.execute("insert into users (f_name, l_name, card_uid, isAdmin, username, password, e_mail) values(?, ?, ?, ?, ?, ?, ?)", (ad, soyad, kart_uid, adminMi, username, password, e_mail))
    connection.commit()
    cursor = connection.execute("select id from users where f_name = ?", (ad,))
    id_ = int(cursor.lastrowid)
    connection.close()
    dsc.createDataSet(id_)
    tr.train()
    tts.girisKayit(ad)
#del user
def kullaniciSil(id_):
    isAdmin = getUserType(id_)

    if(getUserCount() != 1 or not isAdmin):
        path = 'dataSet'
        imagePaths = list()
        connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
        connection.execute("delete from users where id = {}".format(id_))
        connection.commit()
        connection.close()
        for f in os.listdir(path):
            if(f.split(".")[1] == str(id_)):
                imagePaths.append(os.path.join(path, f))
                
        for imagePath in imagePaths:
            os.remove(imagePath)

    else:
        print("\nKullanıcı silme işlemi başarısız.")
        print("Sistemde en az bir yönetici bulunmalıdır.")

def kullanicilariGoster():
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")

    cursor = connection.execute("select * from users")
    
    for row in cursor:
        if(not row[4]):
            print("ID:", row[0])
            print("Adı:", row[1])
            print("Soyadı:", row[2])
            print("Kart UID:", row[3])
            print("*************************")
    
    connection.close()
    
def yoneticileriGoster():
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")

    cursor = connection.execute("select * from users")
    
    for row in cursor:
        if(row[4]):
            print("ID:", row[0])
            print("Adı:", row[1])
            print("Soyadı:", row[2])
            print("Kart UID:", row[3])
            print("Kullanıcı Adı:", row[5])
            print("*************************")
    
    connection.close()

def getAdmins():
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    admins = list()
    cursor = connection.execute("select * from users")
    
    for row in cursor:
        if(row[4]):
            admins.append([row[7], row[1]])
    
    connection.close()
    return admins

def getCardUID():
    try:
        arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout = 10)
    except Exception as e:
        print("Cihaz bağlanamadı.", e)
    time.sleep(2)
    arduino.write(b'uidgonder')
    time.sleep(1)
    uid = str(arduino.readline())[3:14]
    arduino.close()
    return uid

def getAllUIDs():
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    uids = list()
    cursor = connection.execute("select card_uid from users")
    
    for row in cursor:
        uids.append(row[0])
    
    
    connection.close()
    return uids

def getNameFromUID(uid):
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    cursor = connection.execute("select f_name from users where card_uid = ?", (uid,))
    ad = cursor.fetchall()[0][0]
    connection.close()
    return ad

def deleteFromDataset(id_):
    path = 'dataSet'
    imagePaths = list()
    for f in os.listdir(path):
        if(f.split(".")[1] == str(id_)):
            imagePaths.append(os.path.join(path, f))
    
    userCount = getUserCount()
            
    for imagePath in imagePaths:
        os.remove(imagePath)
    
    if(userCount > 1):
        tr.train()

def setConf(conf_deger):
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    cursor = connection.execute("update conf set dogruluk = ? where id = 1", (conf_deger,))
    connection.commit()
    connection.close()

def getConf():
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    cursor = connection.execute("select dogruluk from conf where id = 1")
    dogruluk_degeri = cursor.fetchall()[0][0]
    connection.close()
    return float(dogruluk_degeri)

def getUserCount():
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    cursor = connection.execute("select count(*) from users")
    return cursor.fetchall()[0][0]

def getUserType(id_):
    connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
    cursor = connection.execute("select isAdmin from users where id = ?", (id_,))
    isAdmin = cursor.fetchall()[0][0]
    return isAdmin


