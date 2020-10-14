# -*- coding: utf-8 -*-
import userOperations as user
import datasetCreator as dc
import faceDetector as f
import trainer as tr
import TTS as tts
import cv2
import startProtecting as sp

def adminMenu(name):
    tahmin = 45
    while True:
        print("\nHoşgeldiniz", name)
        print()
        print("1) Kullanıcı Ekle")
        print("2) Yönetici Ekle")
        print("3) Kullanıcıları Göster")
        print("4) Yöneticileri Göster")
        print("5) Kullanıcı Sil")
        print("6) Kalibrasyon Yap")
        print("7) Yüz Tanıma Testi")
        print("8) Korumayı Başlat")
        print("9) Çıkış\n")
        secim = input("Seçiminiz: ")
        if secim == "1":
            ad = input("Adı: ")
            soyad = input("Soyadı: ")
            print("Lütfen kartınızı kart okuyucuya yaklaştırın.")
            kart_uid = user.getCardUID()
            print("Kartınız okundu, UID:", kart_uid)
            input("Kameraya bakın ve ENTER tuşuna basın.")
            user.kullaniciEkle(ad, soyad, kart_uid, False)
            print("\nKullanıcı Başarıyla Eklendi.\n")
        
        elif secim == "2":
            ad = input("Adı: ")
            soyad = input("Soyadı: ")
            print("Lütfen kartınızı kart okuyucuya yaklaştırın.")
            kart_uid = user.getCardUID()
            print("Kartınız okundu, UID:", kart_uid)
            kullanici_adi = input("Kullanıcı Adı: ")
            sifre = input("Şifre: ")
            mail = input("E-Mail: ")
            input("Kameraya bakın ve ENTER tuşuna basın.")
            user.kullaniciEkle(ad, soyad, kart_uid, True, kullanici_adi, sifre, mail)
            print("\nYönetici Başarıyla Eklendi.\n")
        
        elif secim == "3":
            print("\n*************************")
            user.kullanicilariGoster()
            print()
        
        elif secim == "4":
            print("\n*************************")
            user.yoneticileriGoster()
            print()
        
        elif secim == "5":
            user.kullanicilariGoster()
            user.yoneticileriGoster()
            id_ = int(input("\nSilmek istediğiniz kullanıcının ID'sini giriniz: "))
            user.deleteFromDataset(id_)
            user.kullaniciSil(id_)
            
        elif secim == "6":
            print()
            secim = input("Sistemde kayıtlı mısınız? E/H: ").lower()
            if(secim == "e"):
                print()
                user.kullanicilariGoster()
                print("\n*************************")
                user.yoneticileriGoster()
                print()
                id_ = int(input("Lütfen kendi ID'nizi girin: "))
                user.deleteFromDataset(id_)
                input("Birkaç fotoğrafınız çekilecek lütfen kameraya bakarken ENTER tuşuna basın.")
                dc.createDataSet(id_)
                tr.train()
                print("\nŞimdi yüzünüzü tanımayı deneyeceğim.\n")
                input("Kameraya bakarken ENTER tuşuna basın.")
                kisi, conf = f.Recognize()
                print(kisi, conf)
                tahmin = conf + 13
                user.setConf(tahmin)
            
            elif(secim == "h"):
                print()
                ad = input("Adı: ")
                soyad = input("Soyadı: ")
                print("Lütfen kartınızı kart okuyucuya yaklaştırın.")
                kart_uid = user.getCardUID()
                kullanici_adi = input("Kullanıcı Adı: ")
                sifre = input("Şifre: ")
                mail = input("E-Mail: ")

                user.kullaniciEkle(ad, soyad, kart_uid, True, kullanici_adi, sifre, mail)

                print("\nSisteme başarıyla eklendiniz.\n")
                kisi, conf = f.Recognize()
                print(kisi, conf)
                tahmin = conf + 13
                user.setConf(tahmin)
                
        elif secim == "7":
            tahmin = user.getConf()
            print(tahmin)
            kisi, conf = f.Recognize(tahmin) # yüzü 20 kere tahmin edecek ve her tahminini listeye ekleyecek.
            print("Bulunan yüz:", kisi, conf)
            
        elif secim == "8":
            sp.protect(tahmin)
            login_screen()    
        
        
        
        elif secim == "9":
            break
        
        else:
            print("Hatalı seçim yaptınız...\n")
  

def login_screen():
    hak = 3
    while True:
        print("\nMONUR Home Security Solutions®\n")
        print("Menüyü görebilmek için yönetici girişi yapmalısınız.\n")
        print("1) Giriş Yap")
        print("2) Çıkış\n")
        secim = input("Seçiminiz: ")

        if(secim == "1"):
            import sqlite3
            connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")
            cursor = connection.execute("select username, password, f_name from users")
            users = list()

            for row in cursor:
                users.append([row[0], row[1], row[2]])

            connection.close()
            

        
            print()
            username = input("Kullanıcı Adı: ")
            password = input("Şifre: ")
            isLoggedIn = False
            for user in users:
                if username == user[0] and password == user[1]:
                    isLoggedIn = True
                    adminMenu(user[2])

            if not isLoggedIn:
                if hak != 0:
                    print("Giriş Yapılamadı.")
                    print(hak, "hakkınız kaldı.\n")
                    hak -= 1
                else:
                    tts.alarm()
                    break

        elif secim == "2":
            print("\nİyi Günler!")
            exit()

login_screen()