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
    
    # код для парсинга HTML
    return []

if __name__ == "__main__":
    print("Скрипт для сбора данных о погоде в Самаре")
