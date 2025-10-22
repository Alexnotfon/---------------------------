import sqlite3
from contextlib import contextmanager

# Менеджер контекста для автоматического управления соединением с БД
@contextmanager
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Чтобы результаты были в виде словаря
    try:
        yield conn
    finally:
        conn.close()

# Функции для работы с книгами
def get_all_books():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books ORDER BY id')
        books = cursor.fetchall()
        return [dict(book) for book in books]  # Конвертируем в словари

def get_book_by_id(book_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        return dict(book) if book else None

def add_new_book(book_data):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO books (title, author, year, description) 
               VALUES (?, ?, ?, ?)''',
            (book_data['title'], book_data['author'], 
             book_data['year'], book_data.get('description', ''))
        )
        conn.commit()
        return cursor.lastrowid  # Возвращаем ID новой книги

def update_book(book_id, book_data):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE books 
               SET title = ?, author = ?, year = ?, description = ? 
               WHERE id = ?''',
            (book_data['title'], book_data['author'], 
             book_data['year'], book_data.get('description', ''), book_id)
        )
        conn.commit()
        return cursor.rowcount  # Возвращаем количество обновленных строк

def delete_book(book_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        return cursor.rowcount  # Возвращаем количество удаленных строк
