# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Resources
from resources.Users import UserList, User, UserLogin, SecretResource, UserLogoutAccess, UserLogoutRefresh, TokenRefresh
from resources.Roles import RoleList, Role

# instantiate the app
app = Flask(__name__)
#app.config.from_object(config)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
api = Api(app)


# enable CORS
CORS(app)

# users route
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(SecretResource, '/secret')

# roles route
api.add_resource(RoleList, '/role')
api.add_resource(Role, '/role/<role_id>')

#@jwt.token_in_blacklist_loader
#def check_if_token_in_blacklist(decrypted_token):
#    jti = decrypted_token['jti']
#    return is_jti_blacklisted(jti)

if __name__ == '__main__':
    app.run(debug=True, port=int('8084'))