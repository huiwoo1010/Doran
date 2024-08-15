import librosa.display
import matplotlib.pyplot as plt

wordbox = ['가족', '건물', '고양이', '구름', '나무', '남편', '다리', '도서관', '딸기', '라디오', '마음', '모자', '바다', '버스', '사탕', '선물', '수박', '아기', '아파트', '연필', '우유', '자전거', '지우개', '회의', '휴지']

def audiowave_save():
    for word in wordbox:
        audio_path = word+'.wav'
        y, sr = librosa.load(audio_path)
        plt.cla()
        plt.Figure(figsize=(12, 6))
        librosa.display.waveshow(y, sr=sr, alpha=0.5, x_axis=None, marker='')
        plt.savefig(word+".png")


if __name__ == "__main__":
    audiowave_save()