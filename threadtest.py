import threading
import cv2
import moviepy.editor as mp
from playsound import playsound
import pygame

clip=mp.VideoFileClip("sample.mp4")
clip.audio.write_audiofile("sample.mp3")

def vidplay():
    Vid=cv2.VideoCapture('sample.mp4')

    if(Vid.isOpened()==False):
        print("Unable to read camera feed")

    while True:
        ret, color=Vid.read()
        if(color!=[]):
            cv2.imshow('mp4',color)
            cv2.waitKey(2)

def audioplay():
    playsound("sample.mp3")

t=threading.Thread(target=audioplay)
t.start()

vidplay()






