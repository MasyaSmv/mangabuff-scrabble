import json
import requests
from bs4 import BeautifulSoup
import time

# URL для загрузки глав
url = "https://mangabuff.ru/chapters/load"

# Заголовки, которые могут понадобиться для запроса (включая CSRF токен и Cookie, если необходимо)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Csrf-Token': 'P1UslAiTj3fMTm1oa3rFEVlJWAVQA0PwqyG4cHvM',  # Заменить на актуальный CSRF-токен
    'Cookie': 'mangabuff_session=eyJpdiI6Ik1lemxWdENjRGlHbUE3VkYzV0kwVHc9PSIsInZhbHVlIjoiSzlwbkJrblhzYWZZMkx3ejE2ODRRMTczZmlaTGNSSkJUQWVIaGx4WnVrc3F1cy9oaWg0eG5lV1lrN1pzMEVmRUI0Wkdndmx3cmo0eG1JYWppUnMraFRnMnFLOTU3N2drcTh6NU51cWcweHZ1Y29aR0lNSkNUdmQvUktWanVjd24iLCJtYWMiOiIxMmI5ZWJlOGUxZDAzOGFhYWQ2OGVlMWZjMDQwZGY1Mjk3MjExMWZkNzE2NjU1ZGRjOWViODFhNTcwMzBhMTYzIiwidGFnIjoiIn0%3D',
    # Заменить на актуальный Cookie
}


# Функция для отправки POST-запросов и получения глав с пагинацией
def get_chapters_for_manga(manga_id):
    data = {'manga_id': manga_id}  # POST-данные для запроса

    # Отправляем POST-запрос
    response = requests.post(url, headers=headers, data=data)
    chapters = []

    if response.status_code == 200:
        # Получаем HTML контент из поля 'content' в ответе
        content_html = response.json().get('content', '')

        # Разбираем HTML с помощью BeautifulSoup
        soup = BeautifulSoup(content_html, 'html.parser')

        # Ищем все ссылки на главы
        for a in soup.find_all('a', class_='chapters__item'):
            chapter_url = a['href']
            chapters.append(chapter_url)

        print(f'Найдено {len(chapters)} глав.')
    else:
        print(f'Ошибка при получении данных: {response.status_code}')

    return chapters


# Функция для записи данных в файл
def save_to_file(data, filename='manga_chapters.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Основной процесс
def main():
    # Уникальный ID манги
    manga_id = '19560'  # ID манги, полученный из запроса

    # Получаем все главы манги
    all_chapters = get_chapters_for_manga(manga_id)

    # Сохраняем все данные в файл
    save_to_file(all_chapters)

    print(f'Все главы записаны в файл "manga_chapters.json"')


# Запускаем основной процесс
if __name__ == '__main__':
    main()