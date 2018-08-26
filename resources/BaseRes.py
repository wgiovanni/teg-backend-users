from textwrap import dedent
from common.BD import BD
from flask import make_response
from flask_restful import Resource, reqparse

class BaseRes(BD, Resource):
	representasions = {'application/json': make_response}
	parser = reqparse.RequestParser()

	def __init__(self):
		# table_schema es el nombre de la base de datos
		# table_name es el nombre de la tabla
		cols = self.queryAll(dedent("""\
			SELECT *
			FROM INFORMATION_SCHEMA.COLUMNS
			WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s"""), [self.database, self.table])

		for col in cols:
			params = {}
			if col['data_type'] == 'int':
				params['type'] = int
			elif col['data_type'] == 'varchar':
				params['type'] = str
			elif col['data_type'] == 'flot':
				params['type'] = float

			self.parser.add_argument(col['column_name'].lower(), **params)

