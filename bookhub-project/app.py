from flask import Flask, jsonify, request, render_template
from database import get_all_books, get_book_by_id, add_new_book, update_book, delete_book

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница с списком книг"""
    books = get_all_books()
    return render_template('index.html', books=books)

# API endpoints
@app.route('/api/books', methods=['GET'])
def api_get_books():
    """Получить все книги"""
    books = get_all_books()
    return jsonify(books)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
    """Получить книгу по ID"""
    book = get_book_by_id(book_id)
    if book:
        return jsonify(book)
    return jsonify({'error': 'Книга не найдена'}), 404

@app.route('/api/books', methods=['POST'])
def api_add_book():
    """Добавить новую книгу"""
    try:
        new_book_data = request.get_json()
        
        # Проверяем обязательные поля
        if not new_book_data or not new_book_data.get('title') or not new_book_data.get('author'):
            return jsonify({'error': 'Необходимо указать название и автора'}), 400
        
        # Добавляем книгу в базу
        new_id = add_new_book(new_book_data)
        new_book_data['id'] = new_id
        
        return jsonify(new_book_data), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def api_update_book(book_id):
    """Обновить данные книги"""
    try:
        book_data = request.get_json()
        
        # Проверяем, существует ли книга
        if not get_book_by_id(book_id):
            return jsonify({'error': 'Книга не найдена'}), 404
        
        # Обновляем книгу
        updated_count = update_book(book_id, book_data)
        if updated_count > 0:
            return jsonify({'message': 'Книга успешно обновлена'})
        else:
            return jsonify({'error': 'Не удалось обновить книгу'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def api_delete_book(book_id):
    """Удалить книгу"""
    try:
        deleted_count = delete_book(book_id)
        if deleted_count > 0:
            return jsonify({'message': 'Книга успешно удалена'})
        else:
            return jsonify({'error': 'Книга не найдена'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Запускаем сервер в режиме отладки
    app.run(debug=True, host='0.0.0.0', port=5000)
