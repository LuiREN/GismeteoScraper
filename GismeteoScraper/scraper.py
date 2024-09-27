import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime, timedelta

# Словарь для расшифровки облачности
CLOUDINESS = {
    'sun.png': 'Ясно',
    'sunc.png': 'Малооблачно',
    'suncl.png': 'Переменная облачность',
    'dull.png': 'Пасмурно'
}

def get_weather_data(year, month):
    """
    Получает данные о погоде за указанный месяц и год.
    
    Args:
        year (int): Год для получения данных
        month (int): Месяц для получения данных
    
    Returns:
        list: Список списков с данными о погоде за каждый день
    """
    # Формируем URL для запроса данных
    url = f"https://www.gismeteo.ru/diary/4618/{year}/{month:02d}/"
    headers = {"User-Agent": "Mozilla/5.0"}  # Заголовок для имитации браузера

    try:
        # Отправляем GET-запрос к сайту
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем успешность запроса
    except requests.RequestException as e:
        print(f"Ошибка при запросе URL {url}: {e}")
        return []

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Ищем таблицу с данными о погоде
    table = soup.find('table', attrs={
        "align": "center",
        "valign": "top",
        "border": "0"
    })

    if not table:
        print(f"Таблица с данными не найдена на странице {url}")
        return []

    data = []
    # Перебираем строки таблицы, пропуская две строки заголовков
    rows = table.find_all('tr')[2:]
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 11:
            # Извлекаем данные из каждой ячейки
            date = f"{year}-{month:02d}-{cols[0].text.strip()}"
            temp_day = cols[1].text.strip()
            pressure_day = cols[2].text.strip()
            cloudiness_day = get_cloudiness(cols[3])
            wind_day = cols[5].text.strip().split('\n')[-1]
            temp_evening = cols[6].text.strip()
            pressure_evening = cols[7].text.strip()
            cloudiness_evening = get_cloudiness(cols[8])
            wind_evening = cols[10].text.strip().split('\n')[-1]
            # Добавляем данные в список
            data.append([
                date, temp_day, pressure_day, cloudiness_day, wind_day,
                temp_evening, pressure_evening, cloudiness_evening, wind_evening
            ])

    return data

def get_cloudiness(cell):
    """
    Извлекает информацию об облачности из ячейки таблицы.
    
    Args:
        cell (bs4.element.Tag): Ячейка таблицы с данными об облачности
    
    Returns:
        str: Текстовое описание облачности
    """
    # Ищем изображение в ячейке
    img = cell.find('img', class_='screen_icon')
    if img and 'src' in img.attrs:
        # Извлекаем имя файла изображения из атрибута src
        src = img['src'].split('/')[-1]
        # Возвращаем соответствующее описание облачности или 'Неизвестно'
        return CLOUDINESS.get(src, 'Неизвестно')
    return 'Нет данных'

def get_user_input_date(prompt):
    """
    Запрашивает у пользователя ввод даты.
    
    Args:
        prompt (str): Приглашение для ввода
    
    Returns:
        datetime: Объект datetime с введенной датой
    """
    while True:
        date_input = input(prompt)
        try:
            # Пытаемся преобразовать введенную строку в объект datetime
            return datetime.strptime(date_input, "%m.%Y")
        except ValueError:
            print("Некорректный формат даты. Пожалуйста, используйте формат ММ.ГГГГ (например, 01.2001)")

def scrape_weather_history(start_date, end_date):
    """
    Собирает исторические данные о погоде за указанный период.
    
    Args:
        start_date (datetime): Начальная дата периода
        end_date (datetime): Конечная дата периода
    
    Returns:
        list: Список со всеми собранными данными о погоде
    """
    all_data = []
    current_date = start_date
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        print(f"Получение данных за {month:02d}.{year}")
        # Получаем данные за текущий месяц
        month_data = get_weather_data(year, month)
        all_data.extend(month_data)
        # Переходим к следующему месяцу
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)
    return all_data

def save_to_csv(data, filename):
    """
    Сохраняет данные в CSV файл в папке 'dataset'.
    
    Args:
        data (list): Список данных для сохранения
        filename (str): Имя файла для сохранения
    """
    # Создаем папку 'dataset', если она не существует
    dataset_folder = 'dataset'
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    # Формируем полный путь к файлу
    filepath = os.path.join(dataset_folder, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Записываем заголовок CSV файла
        writer.writerow([
            'Дата', 'Температура (день)', 'Давление (день)', 'Облачность (день)', 'Ветер (день)',
            'Температура (вечер)', 'Давление (вечер)', 'Облачность (вечер)', 'Ветер (вечер)'
        ])
        # Записываем данные
        writer.writerows(data)

class WeatherScraper:
    def run(self):
        print("Добро пожаловать в программу сбора данных о погоде в Самаре!")
        start_date = get_user_input_date("Введите начальную дату (ММ.ГГГГ): ")
        end_date = get_user_input_date("Введите конечную дату (ММ.ГГГГ): ")

        if start_date > end_date:
            print("Ошибка: начальная дата не может быть позже конечной даты.")
        else:
            print(f"Начинаем сбор данных о погоде в Самаре с {start_date.strftime('%m.%Y')} по {end_date.strftime('%m.%Y')}...")
            weather_data = scrape_weather_history(start_date, end_date)

            if weather_data:
                filename = f'samara_weather_{start_date.strftime("%Y%m")}-{end_date.strftime("%Y%m")}.csv'
                save_to_csv(weather_data, filename)
                print(f"Данные сохранены в файл dataset/{filename}")
            else:
                print("Не удалось получить данные о погоде.")
