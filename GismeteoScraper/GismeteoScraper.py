import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime, timedelta

# Словарь для расшифровки облачности
# Ключи - названия файлов изображений, значения - текстовое описание
CLOUDINESS = {
    'sun.png': 'Ясно',
    'sunc.png': 'Малооблачно',
    'suncl.png': 'Переменная облачность',
    'dull.png': 'Пасмурно'
}



if __name__ == "__main__":
    print("Добро пожаловать в программу сбора данных о погоде в Самаре!")
    # Запрашиваем у пользователя даты начала и конца периода
    start_date = get_user_input_date("Введите начальную дату (ММ.ГГГГ): ")
    end_date = get_user_input_date("Введите конечную дату (ММ.ГГГГ): ")

    if start_date > end_date:
        print("Ошибка: начальная дата не может быть позже конечной даты.")
    else:
        print(f"Начинаем сбор данных о погоде в Самаре с {start_date.strftime('%m.%Y')} по {end_date.strftime('%m.%Y')}...")
        # Собираем данные о погоде
        weather_data = scrape_weather_history(start_date, end_date)

        if weather_data:
            # Формируем имя файла на основе дат
            filename = f'samara_weather_{start_date.strftime("%Y%m")}-{end_date.strftime("%Y%m")}.csv'
            # Сохраняем данные в CSV файл в папке 'dataset'
            save_to_csv(weather_data, filename)
            print(f"Данные сохранены в файл dataset/{filename}")
        else:
            print("Не удалось получить данные о погоде.")