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


if __name__ == "__main__":
    print("Скрипт для сбора данных о погоде в Самаре")
