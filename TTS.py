from gtts import gTTS
from playsound import playsound

#tts = "Lütfen bir giriş yöntemi seçin."
#speech = gTTS(tts, lang = 'tr')
#speech.save("girisYontemi.mp3")

def girisKayit(name):
    tts = "Hoşgeldin {}".format(name)
    speech = gTTS(tts, lang = 'tr')
    speech.save("sounds/{}.mp3".format(name))
    
def hosgeldin(name):
    playsound("sounds/{}.mp3".format(name))
    
def alarm():
    playsound("sounds/alarm.mp3")