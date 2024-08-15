import cv2
from pydub import AudioSegment
from pydub.playback import play

# 동영상 파일을 열고, 영상 및 오디오 코덱 정보를 가져옴
video_path = 'sample.mp4'
video = cv2.VideoCapture(video_path)
fps = int(video.get(cv2.CAP_PROP_FPS))
frame_size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = int(video.get(cv2.CAP_PROP_FOURCC))

# 오디오 파일을 열음
audio_path = 'sample.mp3'
audio = AudioSegment.from_file(audio_path)

# 동영상 및 오디오 재생을 위한 초기화
play(audio)
cv2.namedWindow(video, cv2.WINDOW_NORMAL)

# 프레임 단위로 동영상 재생
while video.isOpened():
    ret, frame = video.read()
    if ret:
        # 동영상 프레임을 출력
        cv2.imshow(video, frame)

        # ESC 키를 누르면 종료
        if cv2.waitKey(int(1000fps)) & 0xFF == 27 :
            break
    else:
        break

# 종료시 해제
video.release()
cv2.destroyAllWindows()
