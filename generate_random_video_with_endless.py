import os
import numpy as np
import cv2
import shutil
from moviepy.editor import AudioFileClip, concatenate_audioclips
from itertools import cycle

def generate_random_video(width, height, seed):
    # Генерация случайного видео с цветным шумом
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Установка уникального зерна для генератора случайных чисел
    np.random.seed(seed)
    
    while True:
        frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)  # Случайный цветной шум
        yield frame

def generate_random_audio(seed):
    # Генерация случайной аудиодорожки с белым шумом
    np.random.seed(seed)
    
    while True:
        audio_data = np.random.uniform(-1, 1, 44100)  # Произвольный аудиосигнал
        yield audio_data

def save_video_to_desktop(frames_generator, audio_generator, shelf_number, video_number):
    # Создаем директорию "Videos" на рабочем столе, если ее еще нет
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    videos_folder = os.path.join(desktop_path, 'Videos')
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)
    
    # Создаем имя файла для видео
    video_filename = f"shelf{shelf_number}_video{video_number}.mp4"
    destination_path = os.path.join(videos_folder, video_filename)
    
    # Создаем объект VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(destination_path, fourcc, 30, (1280, 720))
    
    # Записываем видео сгенерированными кадрами и аудиодорожкой
    for frame, audio_data in zip(frames_generator, audio_generator):
        out.write(frame)
        
        # Для создания аудиодорожки используем AudioFileClip с буферизацией
        audio_clip = AudioFileClip(np.array(audio_data), fps=44100)
        audio_clip.write_audiofile(destination_path, logger=None, ffmpeg_params=['-vn', '-acodec', 'aac'])
        audio_clip.close()
    
    # Освобождаем объект VideoWriter и закрываем видеофайл
    out.release()
    
    print(f"Видео успешно сохранено на рабочий стол: {video_filename}")

if __name__ == "__main__":
    width = 1280  # Ширина видео
    height = 720  # Высота видео
    
    shelf_input = input("Введите номер стеллажа: ")
    shelf_number = int(shelf_input) if shelf_input != '∞' else float('inf')
    
    video_input = input("Введите номер видео в этом стеллаже: ")
    video_number = int(video_input) if video_input != '∞' else float('inf')
    
    # Генерация видео и аудио на ходу
    frames_generator = generate_random_video(width, height, shelf_number)
    audio_generator = generate_random_audio(shelf_number)
    
    # Сохранение видео на рабочий стол
    save_video_to_desktop(frames_generator, audio_generator, shelf_number, video_number)
