import os
import numpy as np
import cv2

def generate_random_video(width, height, duration):
    # Генерация случайного видео с цветным шумом
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('random_video.mp4', fourcc, 30, (width, height))
    
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

if __name__ == "__main__":
    width = 1280  # Ширина видео
    height = 720  # Высота видео
    duration = 10  # Продолжительность видео в секундах
    
    generate_random_video(width, height, duration)
    
    shelf_number = int(input("Введите номер стеллажа: "))
    video_number = int(input("Введите номер видео в этом стеллаже: "))
    
    save_video_to_desktop('random_video.mp4', shelf_number, video_number)
