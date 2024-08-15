import librosa.display
import matplotlib.pyplot as plt

def audiowave_save():
    audio_path = 'audiosave.wav'
    y, sr = librosa.load(audio_path)
    plt.cla()
    plt.Figure(figsize=(12, 6))
    librosa.display.waveshow(y, sr=sr, alpha=0.5, x_axis=None, marker='')
    plt.savefig("audiowave.png")

    if __name__ == "__main__":
        plt.show()


if __name__ == "__main__":
    audiowave_save()