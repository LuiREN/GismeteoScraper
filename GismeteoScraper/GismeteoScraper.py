import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def get_weather_data(year, month):
    """Получает данные о погоде за указанный месяц и год."""
    url = f"https://www.gismeteo.ru/diary/4618/{year}/{month:02d}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе URL {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', attrs={
        "align": "center",
        "valign": "top",
        "border": "0"
    })

    if not table:
        print(f"Таблица с данными не найдена на странице {url}")
        return []

    data = []
    rows = table.find_all('tr')[2:]  # Пропускаем две строки заголовков
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 11:
            date = f"{year}-{month:02d}-{cols[0].text.strip()}"
            temp_day = cols[1].text.strip()
            pressure_day = cols[2].text.strip()
            wind_day = cols[5].text.strip().split('\n')[-1]
            temp_evening = cols[6].text.strip()
            pressure_evening = cols[7].text.strip()
            wind_evening = cols[10].text.strip().split('\n')[-1]
            data.append([
                date, temp_day, pressure_day, wind_day,
                temp_evening, pressure_evening, wind_evening
            ])

    return data


def scrape_weather_history(start_date, end_date):
    """Собирает исторические данные о погоде за указанный период."""
    all_data = []
    current_date = start_date
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        print(f"Получение данных за {month:02d}.{year}")
        month_data = get_weather_data(year, month)
        all_data.extend(month_data)
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)
    return all_data

def save_to_csv(data, filename):
    """Сохраняет данные в CSV файл."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Дата', 'Температура (день)', 'Давление (день)', 'Облачность (день)', 'Ветер (день)',
            'Температура (вечер)', 'Давление (вечер)', 'Облачность (вечер)', 'Ветер (вечер)'
        ])
        writer.writerows(data)

if __name__ == "__main__":
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
            print(f"Данные сохранены в файл {filename}")
        else:
            print("Не удалось получить данные о погоде.")
