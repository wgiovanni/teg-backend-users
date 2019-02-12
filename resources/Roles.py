from flask_restful import abort
import simplejson as json
from pymysql import DatabaseError
from textwrap import dedent
from resources.BaseRes import BaseRes

class RoleList(BaseRes):
	database = "PRUEBA"
	table = "ROLE"

	def get(self):
		try:
			result = self.queryAll("SELECT * FROM role")
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
		
		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

	def post(self):
		try:
			role = self.parser.parse_args()
			del role['id']
			self.insert('role', role)
			#result = self.queryOne("SELECT TOP 1 * FROM ROLE ORDER BY ID DESC")
			result = self.queryOne("SELECT * FROM role ORDER BY ID DESC LIMIT 1")
			self.commit()
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		
		return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }

class Role(BaseRes):
	database = "PRUEBA"
	table = "ROLE"

	def get(self, role_id):
		try:
			result = self.queryOne("SELECT * FROM role WHERE ID = %s", [role_id])
			if result is None:
				abort(404, message="Resource {} doesn't exists".format(role_id))
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

	def put(self, role_id):
		try:
			role = self.parser.parse_args()
			del role['id']
			self.update('ROLE', role, {'ID': role_id})
			result = self.queryOne("SELECT * FROM role WHERE ID = %s", [role_id])
			if result is None:
				abort(404, message="Resource {} doesn't exist".format(role_id))
			self.commit()
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))

		return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }


	def delete(self, role_id):
		try:
			print(role_id)
			result = self.queryOne("SELECT * FROM role WHERE ID = %s", [role_id])
			print(result)
			if result is None:
				print("Entro")
				abort(404, message="Resource {} doesn't exists".format(role_id))
			else:
				self.remove("DELETE FROM role WHERE ID = %s", [role_id])
				self.commit()
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(404, message="Resource {} doesn't exists".format(role_id))

		return json.dumps(result), 204, { 'Access-Control-Allow-Origin': '*' }

class UserRoleVerifity(BaseRes):
	database = "PRUEBA"
	table = "USER_ROLE"

	def get(self, user_id):
		try:
			result = self.queryOne(dedent("""\
			SELECT r.id, r.name 
			FROM `user_role` AS ur 
			INNER JOIN role AS r 
			ON(ur.id_role = r.id) 
			WHERE id_user = %s 
			ORDER BY r.id DESC 
			LIMIT 1"""), [user_id])
			print(result)

		except Exception as e:
			abort(404, message="Resource {} doesn't exists".format(user_id))
		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

class UserRoleVicerector(BaseRes):
	database = "PRUEBA"
	table = "USER_ROLE"

	def get(self, user_id):
		try:
			result = self.queryOne(dedent("""\
			SELECT r.id, r.name 
			FROM `user_role` AS ur 
			INNER JOIN role AS r 
			ON(ur.id_role = r.id) 
			WHERE id_user = %s 
			ORDER BY r.id ASC 
			LIMIT 1"""), [user_id])
			print(result)

		except Exception as e:
			abort(404, message="Resource {} doesn't exists".format(user_id))
		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

class RoleUser(BaseRes):
	database = "PRUEBA"
	table = "ROLE"

	def get(self, name_role):
		try:
			result = self.queryAll(dedent("""\
			SELECT u.first_name, u.email, u.phone, u.address 
			FROM role as r 
			INNER JOIN user_role as ur 
			ON (r.id = ur.id_role) 
			INNER JOIN user as u 
			ON (ur.id_user = u.id) 
			WHERE r.name = %s"""), [name_role])
			
		except DatabaseError as e:
			self.rollback()
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
		except Exception as e:
			abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))

		return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }