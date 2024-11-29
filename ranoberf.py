import requests
from bs4 import BeautifulSoup
import json
import sqlite3

site = 'https://xn--80ac9aeh6f.xn--p1ai/'


def create_database_and_table(db_name="database.db"):
    try:
        with sqlite3.connect(db_name) as con:
            cur = con.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS ranoberf (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    updated TEXT,
                    chapter TEXT,
                    opened_chapter TEXT,
                    image_path TEXT,
                    type_label TEXT
                )
            ''')
            print(f"Database '{db_name}' and table 'ranoberf' successfully created or already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the database or table: {e}")


def parser():
    bookmark_url = 'https://xn--80ac9aeh6f.xn--p1ai/v3/bookmarks?expand=book.verticalImage,chapter&sort=-updatedAt'
    auth_url = 'https://xn--80ac9aeh6f.xn--p1ai/v3/auth/login'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chromium/80.0.3987.160 Chrome/80.0.3987.163 Safari/537.36'
    }

    login = input('Login: ')
    password = input('Password: ')

    session = requests.Session()
    session.headers.update(headers)

    data = {'email': login, 'password': password}
    response = session.post(auth_url, data=data)
    if response.ok:
        response_data = response.json()
        token = response_data['token']
        csrf_cookie = session.cookies.get('_csrf')

        print(f"Токен: {token}")

        headers.update({
            'Authorization': f'Bearer {token}',
            'X-CSRF-Token': csrf_cookie
        })

        response = session.get(bookmark_url, headers=headers)
        if response.ok:
            with open('bookmarks_ranoberf.json', 'w', encoding='utf-8') as json_file:
                json.dump(response.json(), json_file, ensure_ascii=False, indent=4)
            return response.json()
        else:
            print("Error executing query")
    else:
        print("Authorization error")
    return {}


def print_info_ru(data):
    items = data.get('items', [])

    for item in items:
        book = item.get('book', {})
        chapter = item.get('chapter', {})

        print(f"Книга: {book.get('title')} ({book.get('titleEn', 'Без английского названия')})")
        print(f"  URL: {site + book.get('url')}")
        print(f"  Изображение: {book.get('verticalImage', {}).get('url')}")
        print(f"  Глава: {chapter.get('numberChapter')} - {chapter.get('title')}")
        print(f"  Опубликовано: {chapter.get('publishedAt')}")
        print(f"  Просмотры: {chapter.get('views')}")
        print(f"  Статус: {'Донат' if chapter.get('isDonate') else 'Открытая'}")
        print(f"  Последнее обновление: {item.get('updatedAt')}")
        print("-" * 40)


def print_info_en(data):
    items = data.get('items', [])

    for item in items:
        book = item.get('book', {})
        chapter = item.get('chapter', {})

        print(f"Book: {book.get('title')} ({book.get('titleEn', 'No English name')})")
        print(f"  URL: {site + book.get('url')}")
        print(f"  Image: {book.get('verticalImage', {}).get('url')}")
        print(f"  Chapter: {chapter.get('numberChapter')} - {chapter.get('title')}")
        print(f"  Published: {chapter.get('publishedAt')}")
        print(f"  Views: {chapter.get('views')}")
        print(f"  Status: {'Donate' if chapter.get('isDonate') else 'Open'}")
        print(f"  Last update: {item.get('updatedAt')}")
        print("-" * 40)


def load_books_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def bdsave():
    jsons_line = load_books_from_json('bookmarks_ranoberf.json')

    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            ind = 0
            for i in jsons_line['items']:
                ind += 1
                cur.execute('''
                    INSERT INTO ranoberf (id, title, link, updated, chapter, opened_chapter, image_path, type_label)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ind,
                    i['book']['title'],
                    'https://xn--80ac9aeh6f.xn--p1ai' + i['book']['url'],
                    i['updatedAt'],
                    i['chapter']['numberChapter'],
                    i['chapter']['title'],
                    'https://xn--80ac9aeh6f.xn--p1ai' + i['book']['url'],
                    i['type']

                ))
            con.commit()
            con.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_database_and_table()

    print('Choose language:')
    print('1. Eng\n2. Ru')

    choice = input(': ')
    data = parser()

    if data:
        if choice == '1':
            print_info_en(data)
        elif choice == '2':
            print_info_ru(data)
        else:
            print('Wrong choice')
        bdsave()
