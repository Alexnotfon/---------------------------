import sqlite3
import json

def init_database():
    # Подключаемся к базе данных (файл создастся автоматически)
    connection = sqlite3.connect('database.db')
    
    # Создаем таблицу
    with open('schema.sql') as f:
        connection.executescript(f.read())
    
    # Переносим данные из JSON в базу
    try:
        with open('books.json', 'r', encoding='utf-8') as f:
            books = json.load(f)
        
        cursor = connection.cursor()
        for book in books:
            cursor.execute(
                'INSERT INTO books (title, author, year, description) VALUES (?, ?, ?, ?)',
                (book['title'], book['author'], book['year'], book['description'])
            )
        
        connection.commit()
        print("База данных успешно создана и заполнена данными!")
        
    except FileNotFoundError:
        print("Файл books.json не найден. Создана пустая база данных.")
        connection.commit()
    
    finally:
        connection.close()

if __name__ == '__main__':
    init_database()
