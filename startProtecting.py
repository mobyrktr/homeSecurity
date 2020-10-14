import faceDetector as fd
import motionDetection as md
import TTS as tts
import time
import sendMails as sm
import userOperations as uo
import takePhotos as tp
import serial

leave_time = 5

try:
    arduino = serial.Serial('/dev/ttyUSB0', timeout = 10)
except Exception:
    print("Arduino bağlı değil.")


def alarm():
    print("Alarm!")
    tp.take_photos(5)
    admins = uo.getAdmins()
    sm.sendMails(admins)
    tts.alarm()


def kartOkut():
    uids = uo.getAllUIDs()
    r_uid = uo.getCardUID()
    print(r_uid)
    if(r_uid in uids):
        ad = uo.getNameFromUID(r_uid)
        print(ad)
        tts.hosgeldin(ad)
        return True
    return False


def protect(confidence):
    
    try:
        arduino = serial.Serial('/dev/ttyUSB0', timeout = 10)
    except Exception:
        print("Arduino bağlı değil.")

    print(f"Koruma başlayacak evden çıkmak için {leave_time} saniyeniz var.")
    arduino.write(b'baslat')
    time.sleep(leave_time)

    print("Koruma başladı.")
    print("Hareket Bekleniyor...")
    motion = md.motion_detection()

    if(motion):
        decision_time = 10
        card_reading_time = 10
        face_recognition_time = 10
        hak = 3
        # 5 hak fazla 3 yeterli
        print("Hareket algılandı.")
        tts.hosgeldin("girisYontemi")
        print(f"Bir giriş yöntemi seçmek için {decision_time} saniyeniz var.")
        

        end_time = time.time() + decision_time 
        isEntered = False
        arduino.write(b'buton\n')

        while time.time() < end_time:
            
            secim = str(arduino.readline())[2]    
            
            if(secim == "y"):
                print("\nYüz tanıma seçildi.")
                confidence = uo.getConf()
                while hak > 0:
                    face, conf = fd.Recognize(tahmin = confidence)
                    print(confidence)
                    if face == -1 or conf == 0:
                        print("\nYüz tanınamadı.")
                        hak -= 1
                        print(hak, "hakkınız kaldı.")
                    else:
                        print("\nHoşgeldin", face, conf)
                        tts.hosgeldin(face)
                        timeout_start = time.time() - decision_time
                        isEntered = True
                        break
                
                if hak == 0:
                    print("\nHak kalmadı geçmiş olsun.")
                    end_time = time.time() + decision_time
                    print(f"Kartı okutmak için {decision_time} saniyeniz var.")
                    while time.time() < end_time:
                        isEntered = kartOkut()
                        print("\nKart okundu.")
                        if(isEntered):
                            break
                        else:
                            print("Kayıtlı kart okutulmadı.")
                            alarm()

            elif(secim == "k"):
                print("\nKart Seçildi.")
                end_time = time.time() + decision_time
                print(f"Kartı okutmak için {decision_time} saniyeniz var.")
                while time.time() < end_time:
                    isEntered = kartOkut()
                    if(isEntered):
                        break
                    
                    else:
                        print("Kayıtlı kart okutulmadı.")
                                         
                
                if not isEntered:
                    print("Kart okutma süresi doldu.")
                    alarm()
                    break

            if(isEntered):
                break
        arduino.close()
        if not (secim == "y" or secim == "k"):
            print("Seçim yapmadınız.")
            arduino.close()
            alarm()
