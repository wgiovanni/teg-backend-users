from pyodbc import DatabaseError
from flask_restful import abort
import simplejson as json
from resources.BaseRes import BaseRes

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
