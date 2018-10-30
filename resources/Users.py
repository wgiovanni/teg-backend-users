from flask_restful import abort, Resource
import simplejson as json
from pymysql import DatabaseError
from textwrap import dedent
from resources.BaseRes import BaseRes
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class UserList(BaseRes):
	database = "PRUEBA"
	table = "USER"

	@staticmethod
	def generate_hash(password):
		return sha256.hash(password)

	def get(self):
		try:
			result = self.queryAll(dedent("""\
			SELECT U.id, U.first_name, U.last_name, U.username, U.email, U.password, U.id_role, R.name 
			FROM user AS U INNER JOIN role AS R 
			ON U.id_role = R.id"""))
			#result = self.queryAll("SELECT * FROM PUBLIC.USER")
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))

		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

	def post(self):
		try:
			user = self.parser.parse_args()
			print(user)
			del user['id']
			del user['name']
			user['password'] = self.generate_hash(user['password'])
			self.insert('USER', user)
			#result = self.queryOne("SELECT TOP 1 * FROM USER ORDER BY ID DESC")
			result = self.queryOne("SELECT * FROM USER ORDER BY ID DESC LIMIT 1")
			self.commit()
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		
		return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }

	

class User(BaseRes):
	database = "PRUEBA"
	table = "USER"

	def get(self, user_id):
		try:
			result = self.queryOne("SELECT * FROM USER WHERE ID = %s", [user_id])
			if result is None:
				abort(404, message="Resource {} doesn't exists".format(user_id))
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

	def put(self, user_id):
		try:
			user = self.parser.parse_args()
			del user['id']
			self.update('USER', user, {'ID': user_id})
			result = self.queryOne("SELECT * FROM USER WHERE ID = %s", [user_id])
			if result is None:
				abort(404, message="Resource {} doesn't exist".format(user_id))
			self.commit()
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))

		return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }


	def delete(self, user_id):
		try:
			#print(user_id)
			result = self.queryOne("SELECT * FROM USER WHERE ID = %s", [user_id])
			#print(result)
			if result is None:
				abort(404, message="Resource {} doesn't exists".format(user_id))
			else:
				self.remove("DELETE FROM USER WHERE ID = %s", [user_id])
				self.commit()
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(404, message="Resource {} doesn't exists".format(user_id))

		return json.dumps(result), 204, { 'Access-Control-Allow-Origin': '*' }

	@classmethod
	def is_jti_blacklisted(self, jti):
		query = self.queryOne("SELECT * FROM revoked_token WHERE jti = %s", [jti])
		return bool(query)

class UserLogin(BaseRes):
	database = "PRUEBA"
	table = "USER"

	def post(self):
		try:
			user = self.parser.parse_args()
			print(user)
			result = self.queryOne("SELECT * FROM USER AS u INNER JOIN ROLE AS r ON (u.id_role = r.id) WHERE USERNAME = %s", [user['username']])
			print(result)
			if result is None:
				return json.dumps({ 'message': 'Invalid credentials', 'authenticated': False }), 404
			#if self.verify_hash(result['password'], user['password']):
			if self.verify_hash(user['password'], result['password']):
				access_token = create_access_token(identity = user['username'])
				refresh_token = create_refresh_token(identity = user['username'])
				return json.dumps({'user': result, 
								'message': 'Inicio de session con el usuario {}'.format(result['username']),
								'access_token': access_token,
                				'refresh_token': refresh_token }), 201, { 'Access-Control-Allow-Origin': '*' }
			else:
				return {'message': 'Wrong credentials'}
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
	

	@staticmethod
	def verify_hash(password, hash):
		return sha256.verify(password, hash)


class SecretResource(Resource):
	@jwt_required
	def get(self):
		return {
			'answer': 42
		}

class TokenRefresh(Resource):
	@jwt_refresh_token_required 
	def post(self): 
		current_user = get_jwt_identity() 
		access_token = create_access_token(identity = current_user) 
		return {'access_token': access_token}
    

class UserLogoutAccess(Resource):
	@jwt_required
	def post(self):
		jti = get_raw_jwt()['jti']
		try:
			revoked_token = {'jti': jti}
			self.insert('revoked_token', revoked_token)
			self.commit()
			return {'message': 'Access token has been revoked'}
		except:
			return {'message': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
	@jwt_refresh_token_required
	def post(self):
		jti = get_raw_jwt()['jti']
		try:
			revoked_token = {'jti': jti}
			self.insert('revoked_token', revoked_token)
			self.commit()
			return {'message': 'Access token has been revoked'}
		except:
			return {'message': 'Something went wrong'}, 500

	