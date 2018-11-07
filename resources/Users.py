from flask_restful import abort, Resource, reqparse
from flask import request
import simplejson as json
from flask import make_response
from pymysql import DatabaseError
from textwrap import dedent
from common.BD import BD
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


class UserList(BD, Resource):
	representations = {'application/json': make_response}

	def get(self):
		try:
			result = self.queryAll(dedent("""\
			SELECT U.id, U.first_name, U.last_name, U.username, U.email, U.password, UR.id_role, R.name 
			FROM user AS U INNER JOIN user_role AS UR 
			ON (U.id = UR.id_user) 
			INNER JOIN role AS R 
			ON (UR.id_role = R.id) 
			GROUP BY U.id"""))
			#result = self.queryAll("SELECT * FROM PUBLIC.USER")
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))

		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

	def post(self):
		try:
			user = request.get_json(force=True)
			print(user)
			userPost = {
				"first_name": user['first_name'],
				"last_name": user['last_name'],
				"username": user['username'],
				"email": user['email'],
				"password": user['password']
			}
			#user['password'] = self.generate_hash(user['password'])
			self.insert('USER', userPost)
			#result = self.queryOne("SELECT TOP 1 * FROM USER ORDER BY ID DESC")
			result = self.queryOne("SELECT * FROM USER ORDER BY ID DESC LIMIT 1")
			self.commit()
			print(result)
			roleName = "vicerrector"
			roleVicerector = self.queryOne("SELECT * FROM ROLE WHERE name = %s", [roleName])
			print(roleVicerector)
			#user['id'] es el ID del role
			idRole = user['id_role']
			if roleVicerector is not None:
				if roleVicerector['id'] == idRole:
					print("entro1")
					roleName = "verificador"
					roleVerify = self.queryOne("SELECT * FROM ROLE WHERE name = %s", [roleName])
					userRole = {
						"id_user": result['id'],
						"id_role": idRole 
					}
					self.insert('USER_ROLE', userRole)
					self.commit()
					userRole = {
						"id_user": result['id'],
						"id_role": roleVerify['id'] 
					}
					self.insert('USER_ROLE', userRole)
					self.commit()
				else:
					print("entro2")
					userRole = {
						"id_user": result['id'],
						"id_role": idRole
					}
					self.insert('USER_ROLE', userRole)
					self.commit()
				# datos de auditoria
				audit = {
					"username": user['user'],
					"action": 'Agregó un usuario',
					"module": 'Usuarios'
				}
				self.insert('HISTORY_ACTION', audit)
				self.commit()
			else:
				print("NO hay rol de vicerrector")	
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		
		return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }

class Username(BD, Resource):
	representations = {'application/json': make_response}

	def get(self, username):
		try:
			result = self.queryOne(dedent("""\
			SELECT U.id, U.first_name, U.last_name, U.username, U.email, U.password, U.id_role, R.name 
			FROM user AS U INNER JOIN role AS R 
			ON U.id_role = R.id
			WHERE U.username = %s"""), [username])
			if result is None:
				abort(404, message="Resource {} doesn't exists".format(username))
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }
	

class User(BD, Resource):
	representations = {'application/json': make_response}

	def get(self, user_id):
		try:
			result = self.queryOne(dedent("""\
			SELECT U.id, U.first_name, U.last_name, U.username, U.email, U.password, UR.id_role, R.name 
			FROM USER AS U 
			INNER JOIN user_role AS UR
			ON (U.id = UR.id_user) 
			INNER JOIN role AS R 
			ON (UR.id_role = R.id) 
			WHERE U.id = %s"""), [user_id])
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
			user = request.get_json(force=True)
			print(user)
			#del user['id']
			userUpdate = {
				"first_name": user['first_name'],
				"last_name": user['last_name'],
				"username": user['username'],
				"email": user['email'],
				"password": user['password']
			}
			self.update('USER', userUpdate, {'ID': user_id})
			result = self.queryOne("SELECT * FROM USER WHERE ID = %s", [user_id])
			if result is None:
				abort(404, message="Resource {} doesn't exist".format(user_id))
			self.commit()
			roleName = "vicerrector"
			roleVicerector = self.queryOne("SELECT * FROM ROLE WHERE name = %s", [roleName])
			print(roleVicerector)
			idRole = user['id_role']
			if roleVicerector is not None:
				if roleVicerector['id'] == idRole:
					roleName = "verificador"
					roleVerify = self.queryOne("SELECT * FROM ROLE WHERE name = %s", [roleName])
					self.remove("DELETE FROM USER_ROLE WHERE id_user = %s", [user_id])
					self.commit()
					userRole = {
						"id_user": result['id'],
						"id_role": idRole 
					}
					self.insert('USER_ROLE', userRole)
					self.commit()
					userRole = {
						"id_user": result['id'],
						"id_role": roleVerify['id'] 
					}
					self.insert('USER_ROLE', userRole)
					self.commit()
				else:
					self.remove("DELETE FROM USER_ROLE WHERE id_user = %s", [user_id])
					self.commit()
					userRole = {
						"id_user": result['id'],
						"id_role": idRole
					}
					self.insert('USER_ROLE', userRole)
					self.commit()

				# datos de auditoria
				audit = {
					"username": user['user'],
					"action": 'Modificó un usuario',
					"module": 'Usuarios'
				}
				self.insert('HISTORY_ACTION', audit)
				self.commit()
			else:
				print("NO hay rol de vicerrector")		
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))

		return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }


	def delete(self, user_id):
		try:
			jsonData = request.get_data(cache=False, as_text=False, parse_form_data=False)
			jsonData = json.loads(jsonData)
			result = self.queryOne("SELECT * FROM USER WHERE ID = %s", [user_id])
			#print(result)
			if result is None:
				abort(404, message="Resource {} doesn't exists".format(user_id))
			else:
				userRole = self.queryAll("SELECT * FROM USER_ROLE WHERE id_user = %s", [user_id])
				if userRole is None:
					abort(404, message="Resource {} doesn't exists".format(user_id))
				else:
					self.remove("DELETE FROM USER_ROLE WHERE id_user = %s", [user_id])
					self.commit()
				self.remove("DELETE FROM USER WHERE ID = %s", [user_id])
				self.commit()
				# datos de auditoria
				audit = {
					"username": jsonData['user'],
					"action": 'Eliminó un usuario',
					"module": 'Usuarios'
				}
				self.insert('HISTORY_ACTION', audit)
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

class UserLogin(BD, Resource):
	representations = {'application/json': make_response}

	@staticmethod
	def generate_hash(password):
		return sha256.hash(password)

	def post(self):
		try:
			jsonData = request.get_json(force=True)
			
			user = {
				"username": jsonData['username'],
				"password": jsonData['password']
			}
			print(user)
			audit = {
				"username": jsonData['username'],
				"action": "Ingreso al sistema",
				"module": "Usuarios"
			}
			result = self.queryOne(dedent("""\
			SELECT U.id, U.first_name, U.last_name, U.username, U.email, U.password, UR.id_role, R.name 
			FROM USER AS U 
			INNER JOIN user_role AS UR
			ON (U.id = UR.id_user) 
			INNER JOIN role AS R 
			ON (UR.id_role = R.id) 
			WHERE U.username = %s"""), [user['username']])
			print(result)
			if result is None:
				return json.dumps({ 'message': 'Invalid credentials', 'authenticated': False }), 404
			#if self.verify_hash(result['password'], user['password']):
			if self.verify_hash(user['password'], self.generate_hash(result['password'])):
				self.insert('HISTORY_ACTION', audit)
				self.commit()
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

	