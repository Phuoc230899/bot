import simpleaudio as sa
from gtts import gTTS
import playsound
import os
import time
def hello(text):
    tts = gTTS(text,lang ='vi')
    tts.save('hello.mp3')
    playsound.playsound('hello.mp3')
    time.sleep(1)
    os.remove('hello.mp3')

# hello("Thuỳ Linh - Nữ sinh năm 3 với gương mặt cực kỳ xinh xắn đến từ khoa Luật")