from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Serializer, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#class BaseModel(db.Model):
#    """Base data model for all objects"""
#    __abstract__ = True

#    def __init__(self, *args):
#        super().__init__(*args)

#    def __repr__(self):
#        """Define a base way to print models"""
#        return '%s(%s)' % (self.__class__.__name__, {
#            column: value
#            for column, value in self._to_dict().items()
#        })

#    def json(self):
#        """
#                Define a base way to jsonify models, dealing with datetime objects
#        """
#        return {
#            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
#            for column, value in self._to_dict().items()
#        }

class UserSerializer(Serializer):
    id= fields.Integer()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.String()
    password = fields.String()



class User(db.Model):
    """Model for the user table"""
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key = True)
    firstName = db.Column('first_name', db.String())
    lastName = db.Column('last_name', db.String())
    email = db.Column('email', db.String())
    password = db.Column('password', db.String())




    #def __init__(self, id, firstName, lastName, email, password):
    #    self.id = id
    #    self.firstName = firstName
    #    self.lastName = lastName
    #    self.email = email
    #    self.password = password