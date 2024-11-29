# Ranoberf Parser and Database Manager

This project is a parser and database manager for bookmarks from the website [ранобэ.рф](https://ранобэ.рф)/ [https://xn--80ac9aeh6f.xn--p1ai/](https://xn--80ac9aeh6f.xn--p1ai/). It allows users to log in, retrieve bookmarks, save them in a JSON file, and store them in an SQLite database for further analysis.

## Features

- **Authorization:** Logs into the website using your credentials.
- **Bookmark Parsing:** Retrieves bookmarks and their metadata from your account.
- **JSON Export:** Saves the parsed data into a formatted JSON file.
- **Database Integration:** Creates an SQLite database and stores the parsed data into a table.
- **Multilingual Output:** Provides output in English and Russian, depending on user choice.

## Requirements

- Python 3.7+
- The following Python libraries:
  - `requests`
  - `BeautifulSoup` (from `bs4`)
  - `sqlite3` (built-in with Python)

You can install the required libraries using pip:
```bash
pip install requests beautifulsoup4
```
## Usage

1. Clone the repository:

```bash
git clone https://github.com/Azaki21421/pars_ranoberf
cd pars_ranoberf
```

2. Run the script:

```bash
python ranoberf.py
```

3. Follow the prompts:

- Enter your login credentials for ранобэ.рф.
- Choose your preferred language (English or Russian).
- The script will retrieve your bookmarks, save them in bookmarks_ranoberf.json, and store them in the SQLite database database.db.
## Files
- **script.py**: The main script containing all the functions.
- **bookmarks_ranoberf.json**: JSON file generated with the parsed data.
- **database.db**: SQLite database where parsed data is stored.

## Data Structure
The parsed data includes the following fields:

- **title**: The title of the book.
- **link**: The URL of the book on the website.
- **updated**: The last update timestamp.
- **chapter**: The chapter number.
- **opened_chapter**: The chapter title.
- **image_path**: The URL of the book's image.
- **type_label**: The type or category of the bookmark.

## Examples

### English Output
```yaml

Book: Title (No English name)
  URL: https://ранобэ.рф/book-url
  Image: https://ранобэ.рф/image-url
  Chapter: 12 - Chapter Title
  Published: 2024-11-01
  Views: 1000
  Status: Open
  Last update: 2024-11-01T10:00:00Z
----------------------------------------
```
### Russian Output
```yaml
Книга: Название (Без английского названия)
  URL: https://ранобэ.рф/book-url
  Изображение: https://ранобэ.рф/image-url
  Глава: 12 - Название главы
  Опубликовано: 2024-11-01
  Просмотры: 1000
  Статус: Открытая
  Последнее обновление: 2024-11-01T10:00:00Z
----------------------------------------
```
