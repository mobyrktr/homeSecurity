# -*- coding: utf-8 -*-
from gtts import gTTS
from playsound import playsound
#tts = "Lütfen bir giriş yöntemi seçin."
#speech = gTTS(tts, lang = 'tr')
#speech.save("girisYontemi.mp3")

def girisKayit(name):
    tts = f"Hoşgeldin {name}"
    speech = gTTS(tts, lang = 'tr')
    speech.save(f"sounds/{name}.mp3")
    
def hosgeldin(name):
    playsound(f"sounds/{name}.mp3")
    
def alarm():
    playsound("sounds/alarm.mp3")
