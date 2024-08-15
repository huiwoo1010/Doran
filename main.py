import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk
import argparse
import audiorecognize
import audiowavemaker
import pyaudio
import wave
import webcamrecord

root = tk.Tk()
root.title('도란도란')
root.geometry('1080x720+0+0')
root.resizable(False, False)

main_background = tk.PhotoImage(file='image\\background.png')
title_background = tk.PhotoImage(file='image\\title.png')
message_background = tk.PhotoImage(file='image\\information.png')
start = tk.PhotoImage(file='image\\startbutton.png')
word_study = tk.PhotoImage(file='image\\wordstudy.png')
score_bubble = tk.PhotoImage(file='image\\score.png')

record_start = tk.PhotoImage(file='image\\recordstart.png')
record_stop = tk.PhotoImage(file='image\\recordstop.png')
record_check = tk.PhotoImage(file='image\\checkbutton.png')
mic_button = tk.PhotoImage(file='image\\mic.png')

stage_number = 0
word_index = -1
word_title = '가족'
frm_record = None
score = 97
camera_flag=False

wordbox = ['가족', '건물', '고양이', '구름', '나무', '남편', '다리', '도서관', '딸기', '라디오', '마음', '모자', '바다', '버스', '사탕', '선물', '수박', '아기', '아파트', '연필', '우유', '자전거', '지우개', '회의', '휴지']

wordtitle=tk.PhotoImage(file='image\\titles\\title_'+ word_title +'.png')
comment_image=tk.PhotoImage(file='image\\comments\\80.png')
b = tk.PhotoImage(file='voice/' + word_title + '.png')


def open_frame(frame):
    try:
        frame.tkraise()
    except IndexError:
        pass


def open_program():
    global stage_number, word_index
    stage_number = 0
    word_index = -1
    open_frame(start_page)


def start_program():
    open_page()


def open_page():
    global stage_number, word_index
    word_index += 1
    stage_number += 1
    try:
        open_frame(MainPage(root, wordbox[word_index]))
    except IndexError:
        pass


def jump_page(x):
    global stage_number, word_index
    try:
        word_index = x[0]
        open_frame(MainPage(root, wordbox[word_index]))
        stage_number += 1
    except IndexError:
        pass


def fake():
    pass


class MainPage(tk.Frame):
    def __init__(self, master, word):
        global stage_number, frm_record, word_title, score
        word_title = word
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0, sticky="nsew")
        tk.Label(self, image=main_background).pack()
        wordtitle.config(file='image/titles/title_' + word + '.png')
        tk.Label(self, image=wordtitle, bg="#F9F3F1").place(x=50, y=40)
        #tk.Label(self, text="<따라해 보세요> : 학습할 단어를 발음하면서 영상 녹화, 음성 녹음을 순서대로 한 번씩 진행해주세요.", bg="#F9F3F1",
        #         font=("Arial", 15)).place(x=40, y=450)
        # tk.Label(self, text="오늘 학습한 단어: %d 개" % stage_number, bg="#F9F3F1").place(x=800, y=17)

        frm_Listbox = tk.Frame(self, bg="#F9F3F1")
        frm_listbox = tk.Frame(frm_Listbox, bg='#F9F3F1')
        word_listbox = tk.Listbox(frm_listbox, width=18, height=14, selectmode="single")
        for i in range(len(wordbox)):
            word_listbox.insert(i, wordbox[i])
        scrollbar = tk.Scrollbar(frm_listbox, orient="vertical", command=word_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        word_listbox.config(yscrollcommand=scrollbar.set)
        word_listbox.pack(side="left")
        frm_listbox.pack(side="top")
        btn_to_jump = tk.Button(frm_Listbox, text="  선택  ",
                                command=lambda: [self.close_camera(), jump_page(word_listbox.curselection())])
        btn_to_jump.pack(pady=10, side="top", anchor="center")
        frm_Listbox.place(x=900, y=130)

        frm_video = tk.Frame(self, bg="white", width=400, height=300)
        frm_video.place(x=50, y=130)

        self.canvas_record = tk.Canvas(self, bg="white", width=410, height=145)
        self.canvas_record.place(x=470, y=285)

        # self.frm_voice = tk.Frame(self, bg="pink", width=410, height=145)
        # self.frm_voice.place(x=470, y=130)
        # self.canvas_mobum = tk.Canvas(self, bg="white", width=410, height=145)
        # self.canvas_mobum.place(x=470, y=130)
        b.config(file='voice/' + word + '.png')
        voice_wave = tk.Label(self, image=b)
        voice_wave.place(x=470, y=130)
        # voice_wave = tk.Label(self.canvas_mobum, image=b)
        # voice_wave.pack()

        btn_to_quit = tk.Button(self, text=" 나가기 ", command=lambda:[self.close_camera(), open_program()])
        btn_to_quit.place(x=1010, y=10)

        chunk = 1024
        format = pyaudio.paInt16
        channels = 2
        rate = 44100
        wave_output_filename = "audiosave.wav"
        self.p = pyaudio.PyAudio()
        self.wf = wave.open(wave_output_filename, "wb")
        self.wf.setnchannels(channels)
        self.wf.setsampwidth(self.p.get_sample_size(format))
        self.wf.setframerate(rate)
        self.audio_record_flag = False
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  input=True, stream_callback=self.callback)

        # recorder
        self.vid = VideoCapture(0)
        self.ok = False
        self.done = False

        self.vid.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
        self.vid.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 192)

        self.canvas = tk.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.place(x=50, y=500)

        self.btn_video = tk.Button(self, image=record_start, command=lambda: (self.open_camera()))
        self.btn_video.place(x=320, y=660)

        self.delay = 10
        self.update()

    def audio_recog(self):
        user_text = audiorecognize.recognize()
        global stage_number, word_index, frm_record
        try:
            text_label = tk.Label(self, text=user_text)
            text_label.place(x=0, y=0)
            audiowavemaker.audiowave_save()
            audio_img = PIL.Image.open('audiowave.png')
            resized_audioimg = audio_img.resize((410, 145))
            a = PIL.ImageTk.PhotoImage(resized_audioimg)
            audio_wave = tk.Label(self.canvas_record, image=a)
            audio_wave.pack()
        except IndexError:
            pass
        self.set_command()

    def set_command(self):
        frm_score = tk.Frame(self, width=500, height=300, bg="#F9F3F1")
        tk.Label(frm_score, image=score_bubble).place(x=0,y=0)
        score_label = tk.Label(frm_score, text="%d" % score, font=("G마켓 산스", 55), bg="#FFFFFF")
        score_label.place(x=40,y=115)
        if score >= 80:
            comment_image.config(file='image/comments/80.png')
        elif score >= 60:
            comment_image.config(file='image/comments/60.png')
        elif score >= 40:
            comment_image.config(file='image/comments/40.png')
        elif score >= 20:
            comment_image.config(file='image/comments/20.png')
        elif score >= 0:
            comment_image.config(file='image/comments/0.png')
        comment_label = tk.Label(frm_score, image=comment_image, bg="#F9F3F1")
        comment_label.place(x=200,y=110)
        frm_score.place(x=500, y=460)

    def callback(self, in_data, frame_count, time_info, status):
        self.wf.writeframes(in_data)
        if self.audio_record_flag:
            return (in_data, pyaudio.paContinue)
        else:
            return (in_data, pyaudio.paComplete)

    def open_camera(self):
        global camera_flag
        camera_flag=True
        self.btn_video.config(image=record_stop, command=self.close_camera)
        self.ok = True

        self.audio_record_flag = True
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  input=True, stream_callback=self.callback)
        self.stream.start_stream()

        print("camera opened => Recording")

    def close_camera(self):
        # self.btn_video.config(image=record_start, command=self.open_camera)
        global camera_flag
        self.btn_video.config(image=record_check, command=fake)
        self.ok = False
        self.vid.vid.release()
        self.vid.out.release()
        self.done = True
        if (camera_flag == True):
            self.stream.stop_stream()
            self.stream.close()
            self.audio_recog()
        print("camera closed => Not Recording")
        camera_flag=False

    def update(self):
        if not self.done:
            ret, frame = self.vid.get_frame()
            if self.ok:
                self.vid.out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                print("화면 저장")

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.after(self.delay, self.update)


class VideoCapture:
    def __init__(self, video_source=0):

        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        args = CommandLineParser().args
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        self.fourcc = VIDEO_TYPE[args.type[0]]

        STD_DIMENSIONS = {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        res = STD_DIMENSIONS[args.res[0]]
        print(args.name, self.fourcc, res)
        self.width, self.height = res
        self.width /= 2.5
        self.height /= 2.5
        # now = datetime.datetime.now().strftime("%y.%m.%d_%H-%M-%S")
        self.out = cv2.VideoWriter('videosave' + '.' + args.type[0], self.fourcc, 30,
                                   (int(self.width), int(self.height)))
        print("저장")

        self.vid.set(3, self.width)
        self.vid.set(4, self.height)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                resize_frame = cv2.resize(frame, (int(self.width), int(self.height)), interpolation=cv2.INTER_CUBIC)
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(resize_frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            pass

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()


class CommandLineParser:

    def __init__(self):
        parser = argparse.ArgumentParser(description='Script to record videos')

        parser.add_argument('--type', nargs=1, default=['avi'], type=str,
                            help='Type of the video output: for now we have only AVI & MP4')

        parser.add_argument('--res', nargs=1, default=['480p'], type=str,
                            help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')

        parser.add_argument('--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')

        self.args = parser.parse_args()


start_page = tk.Frame(root)
message_page = tk.Frame(root)

start_page.grid(row=0, column=0, sticky="nsew")
message_page.grid(row=0, column=0, sticky="nsew")

# 시작 페이지 설계
tk.Label(start_page, image=title_background).pack()
btnTostart = tk.Button(start_page, image=start, command=lambda: open_frame(message_page))
btnTostart.place(x=305, y=630)

# 설명 페이지 설계
tk.Label(message_page, image=message_background).pack()
btnTostudy = tk.Button(message_page, image=word_study, command=lambda: start_program())
btnTostudy.place(x=310, y=630)


open_frame(start_page)
root.mainloop()
