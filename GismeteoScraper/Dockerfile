# Используем официальный образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY main.py .
COPY scraper.py .

# Создаем директорию для сохранения данных
RUN mkdir dataset

# Команда для запуска приложения
CMD ["python", "main.py"]