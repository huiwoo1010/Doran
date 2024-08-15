import speech_recognition as sr
from pyaudio import *
import wave
import numpy as np

def recognize():
    r = sr.Recognizer()
    korean_audio = sr.AudioFile('audiosave.wav')

    with korean_audio as source:
        audio = r.record(source)

    return r.recognize_google(audio_data=audio, language='ko-KR')


if __name__ == "__main__":
    print(recognize())
