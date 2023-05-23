from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_Schema

api = Blueprint( 'api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return {'digital': 'library'}

# Create book
@api.route('/books',methods=['POST'])
@token_required
def create_book(current_user_token):
    book_title = request.json['book_title']
    author = request.json  ['author']
    genre = request.json['genre']
    isbn = request.json['isbn']
    length = request.json['length']
    cover_type = request.json['cover_type']
    user_token = current_user_token.token

    print (f'BIG TESTER: {current_user_token.token}')

    book = Book(book_title, author, genre, isbn, length, cover_type, user_token = user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# Get all books
@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_Schema.dump(books)
    return jsonify(response)

# Get single book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)


# Update book
@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.book_title = request.json['book_title']
    book.author = request.json['author']
    book.genre = request.json['genre']
    book.isbn = request.json ['isbn']
    book.length = request.json ['length']
    book.cover_type = request.json['cover_type']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)
    
# Delete book
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)