import pygame
import sys

pygame.init()

# 동영상 파일 경로와 크기 설정
video_path = 'sample.mp4'
width = 640
height = 480

# 동영상 파일 열기
pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.load('sample.mp3')
pygame.mixer.music.play()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Video Player')

# 동영상 재생 준비
video = pygame.movie.Movie(video_path)
video.set_display(screen, pygame.Rect(0, 0, width, height))
video.play()

# 이벤트 처리 루프
while video.get_busy():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            video.stop()
            pygame.quit()
            sys.exit()

    pygame.display.update()