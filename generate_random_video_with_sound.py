import os
import numpy as np
import cv2
import shutil
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

def generate_random_video(width, height, duration, seed):
    # Генерация случайного видео с цветным шумом
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('random_video.mp4', fourcc, 30, (width, height))
    
    # Установка уникального зерна для генератора случайных чисел
    np.random.seed(seed)
    
    for _ in range(duration * 30):  # 30 FPS
        frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)  # Случайный цветной шум
        video.write(frame)
    
    video.release()

def save_video_to_desktop(video_path, shelf_number, video_number):
    # Создаем директорию "Videos" на рабочем столе, если ее еще нет
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    videos_folder = os.path.join(desktop_path, 'Videos')
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)
    
    # Создаем имя файла для видео
    video_filename = f"shelf{shelf_number}_video{video_number}.mp4"
    destination_path = os.path.join(videos_folder, video_filename)
    
    # Копируем видео в папку Videos на рабочем столе
    shutil.copy(video_path, destination_path)
    
    print(f"Видео успешно сохранено на рабочий стол: {video_filename}")

def add_audio(video_path):
    # Создаем аудиофайл с белым шумом такой же продолжительности, как и видео
    duration = VideoFileClip(video_path).duration
    audio = AudioFileClip('white_noise.wav').subclip(0, duration)

    # Загружаем видео и добавляем к нему аудио
    video = VideoFileClip(video_path)
    video = video.set_audio(audio)
    
    # Сохраняем видео с звуком
    video_with_audio_path = 'random_video_with_audio.mp4'
    video.write_videofile(video_with_audio_path, codec='libx264', audio_codec='aac')
    
    return video_with_audio_path

if __name__ == "__main__":
    width = 1280  # Ширина видео
    height = 720  # Высота видео
    
    shelf_number = int(input("Введите номер стеллажа: "))
    video_number = int(input("Введите номер видео в этом стеллаже: "))
    
    # Используем номер стеллажа как уникальное зерно для генерации случайного шума
    generate_random_video(width, height, shelf_number, seed=shelf_number)
    video_path = 'random_video.mp4'
    
    # Добавляем звук к видео
    video_with_audio_path = add_audio(video_path)
    
    # Сохраняем видео с звуком на рабочий стол
    save_video_to_desktop(video_with_audio_path, shelf_number, video_number)
