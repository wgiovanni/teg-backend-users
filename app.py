# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
#from flask_marshmallow import Marshmallow
#from flask_sqlalchemy import SQLAlchemy
#import config
from flask_restful import Api
#from Users import Users, User
#from user_schema import UserSchema
#from user import UserSchema
from flask_jwt_extended import JWTManager
from resources.Users import UserList, User, Login

# instantiate the app
app = Flask(__name__)
#app.config.from_object(config)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
api = Api(app)
#ma = Marshmallow(app)


# configuration database POSTGRESQL
#POSTGRES = {
#    'user': 'postgres',
#    'pw': '123456',
#    'db': 'prueba',
#    'host': 'localhost',
#    'port': '5432',
#}
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/prueba'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
#db.init_app(app)

# enable CORS
CORS(app)


#user_schema = UserSchema()
#users_schema = UserSchema(many=True)

#users route
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<user_id>')
api.add_resource(Login, '/auth')

# sanity check route
#@app.route('/ping', methods=['GET'])
#def ping_pong():
#    return jsonify('pong!')


#@app.route('/user', methods=['GET'])
#def findAll():
#    users = User.query.all()
#    result = users_schema.dumps(users)
#    return jsonify(result.data)

#@app.route('/user/<user_id>', methods=['GET'])
#def findById(user_id):
#    user = User.query.get(user_id)
#    return user_schema.jsonify(user)

#@app.route('/user/<user_id>', methods=['PUT'])
#def update(user_id):
#    user = User.query.get(user_id)
#    firstName = request.json['firstName']
#   lastName = request.json['lastName']
#    email = request.json['email']
#    password = request.json['password']

#    user.firstName = firstName
#    user.lastName = lastName
#    user.email = email
#    user.password = password

#    db.session.commit()
#    return user_schema.jsonify(user)

#@app.route('/user', methods=['POST'])
#def save():
#    firstName = request.json['firstName']
#    lastName = request.json['lastName']
#    email = request.json['email']
#    password = request.json['password']

#    user = User(firstName, lastName, email, password)

#    db.session.add(user)
#    db.session.commit()

#    return user_schema.jsonify(user)

#@app.route('/user/<user_id>', methods=['DELETE'])
#def delete(user_id):
#    user = User.query.get(user_id)
#    db.session.delete(user)
#    db.session.commit()

#    return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)