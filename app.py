# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Resources
from resources.Users import UserList, User, Login
from resources.Roles import RoleList, Role

# instantiate the app
app = Flask(__name__)
#app.config.from_object(config)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
api = Api(app)


# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# users route
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<user_id>')
api.add_resource(Login, '/auth')

# roles route
api.add_resource(RoleList, '/role')
api.add_resource(Role, '/role/<role_id>')

if __name__ == '__main__':
    app.run(debug=True)