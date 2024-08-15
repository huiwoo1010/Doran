import wave
import pyaudio
from PIL import ImageGrab
import numpy as np
import cv2
import time

chunk = 1024
format = pyaudio.paInt16
channels = 2
rate = 44100
wave_output_filename = "audiosave.wav"
p = pyaudio.PyAudio()
wf = wave.open(wave_output_filename, "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(format))
wf.setframerate(rate)
audio_record_flag = True


def callback(in_data, frame_count, time_info, status):
    wf.writeframes(in_data)
    if audio_record_flag:
        return (in_data, pyaudio.paContinue)
    else:
        return (in_data, pyaudio.paComplete)


def record():
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(),
                    input=True, stream_callback=callback)
    image = ImageGrab.grab()  # Get the current screen
    width = image.size[0]
    height = image.size[1]
    print("width:", width, "height:", height)
    print("image mode:", image.mode)
    k = np.zeros((width, height), np.uint8)
    fourcc = cv2.VideoWriter_fourcc(*"divx")  # encoding format
    video = cv2.VideoWriter("videosave.avi", fourcc, 9.5, (width, height))

    print("video recording !!!!!")
    stream.start_stream()
    print("audio recording !!!!!")
    record_count = 0
    while True:
        img_rgb = ImageGrab.grab()
        img_bgr = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)  # Convert to opencv's bgr format
        video.write(img_bgr)
        record_count += 1
        if (record_count > 50):
            break
        print(record_count, time.time())
    global audio_record_flag
    audio_record_flag = False
    while stream.is_active():
        time.sleep(1)
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()
    print("audio recording done !!!!!")
    video.release()
    cv2.destroyAllWindows()
    print("video recording done !!!!!")

if __name__=='__main__':
    record()