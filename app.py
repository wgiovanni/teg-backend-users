# -*- coding: utf-8 -*-
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
ma = Marshmallow(app)

# configuration database POSTGRESQL
POSTGRES = {
    'user': 'postgres',
    'pw': '123456',
    'db': 'prueba',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#db.init_app(app)

# enable CORS
CORS(app)

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


class User(db.Model):
    """Model for the user table"""
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key = True)
    firstName = db.Column('first_name', db.String())
    lastName = db.Column('last_name', db.String())
    email = db.Column('email', db.String())
    password = db.Column('password', db.String())

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
        
# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        users = User.query.all()
        result = users_schema.dumps(users)
        return jsonify(result.data)
    return jsonify(response_object)

@app.route('/user', methods=['GET'])
def findAll():
    users = User.query.all()
    result = users_schema.dumps(users)
    return jsonify(result.data)

@app.route('/user/<user_id>', methods=['GET'])
def findById(user_id):
    user = User.query.get(user_id)
    return user_schema.jsonify(user)

@app.route('/user/<user_id>', methods=['PUT'])
def update(user_id):
    user = User.query.get(user_id)
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']

    user.firstName = firstName
    user.lastName = lastName
    user.email = email
    user.password = password

    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/user', methods=['POST'])
def save():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']

    user = User(firstName, lastName, email, password)

    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/user/<user_id>', methods=['DELETE'])
def delete(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        # TODO: refactor to a lambda and filter
        return_book = ''
        for book in BOOKS:
            if book['id'] == book_id:
                return_book = book
        response_object['book'] = return_book
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'price': post_data.get('price')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


if __name__ == '__main__':
    app.run()