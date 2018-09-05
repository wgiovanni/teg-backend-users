from pyodbc import DatabaseError
from flask_restful import abort
import simplejson as json
from resources.BaseRes import BaseRes
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class UserList(BaseRes):
	database = "PRUEBA"
	table = "USER"

	def get(self):
		try:
			result = self.queryAll("SELECT * FROM USER")
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
		
		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

	def post(self):
		try:
			user = self.parser.parse_args()
			del user['id']
			self.insert('USER', user)
			#result = self.queryOne("SELECT TOP 1 * FROM USER ORDER BY ID DESC")
			result = self.queryOne("SELECT * FROM USER ORDER BY ID DESC LIMIT 1")
			self.commit()
		except DatabaseError as e:
			self.rollback()
			bort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
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
			print(user_id)
			result = self.queryOne("SELECT * FROM USER WHERE ID = %s", [user_id])
			print(result)
			if result is None:
				print("Entro")
				abort(404, message="Resource {} doesn't exists".format(user_id))
			else:
				self.remove("DELETE FROM USER WHERE ID = %s", [user_id])
				self.commit()
		except DatabaseError as e:
			self.rollback()
			#print("Entro 1")
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			#print("Entro 2")
			#abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
			abort(404, message="Resource {} doesn't exists".format(user_id))

		return json.dumps(result), 204, { 'Access-Control-Allow-Origin': '*' }

class Login(BaseRes):
	database = "PRUEBA"
	table = "USER"

	def post(self):
		try:
			user = self.parser.parse_args()
			print(user)
			result = self.queryOne("SELECT * FROM USER WHERE EMAIL = %s", [user['email']])
			if not result:
				abort(404, message="User {} doesn't exists".format(user['email']))
			if self.verify_hash(result['password'], user['password']):
				access_token = create_access_token(identity = user['email'])
				refresh_token = create_refresh_token(identity = user['email'])
			else:
				abort(404, message="Acceso Prohibido {} doesn't exists".format(user['id']))
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		
		return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }

	@staticmethod
	def generate_hash(password):
		return sha256.hash(password)

	@staticmethod
	def verify_hash(password, hash):
		return sha256.verify(password, hash)