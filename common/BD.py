import pymysql
import configparser

class BD:
	conn = None

	def connect(self):
		if self.conn is None:
			config = configparser.ConfigParser()
			if not config.read('user.properties'):
				raise Exception ('Error leyendo el archivo user.properties')

			#self.conn = pymysql.connect(config['BD']['connstring'])
			self.conn = pymysql.connect(host='localhost', user='root', password='', db='prueba')

	def queryAll(self, sql: str, params: list=[], columns: list=None):
		self.connect()
		cursor = self.conn.cursor()
		cursor.execute(sql, params)
		rows = cursor.fetchall()
		if columns is None:
			columns = [column[0].lower() for column in cursor.description]
		cursor.close()
		return [dict(zip(columns, row)) for row in rows]

	def queryOne(self, sql: str, params: list=[], columns: list=None):
		self.connect()
		cursor = self.conn.cursor()
		cursor.execute(sql, params)
		row = cursor.fetchone()
		if row is None:
			return None
		if columns is None:
			columns = [column[0].lower() for column in cursor.description]
		cursor.close()
		return dict(zip(columns, row))

	def insert(self, table: str, datos: dict=None, columns=None, values: list=None):
		self.connect()
		cursor = self.conn.cursor()

		if datos is not None:
			columns = []
			values = []
			for col, val in datos.items():
				columns.append(col)
				values.append(val)

		if isinstance(columns, str):
			columns = "("+columns+")"
		elif isinstance(columns, list):
			columns = "("+", ".join(columns)+")"

		if isinstance(values[0], (list, tuple)):
			marks = "?" + (",?" * (len(values[0]) - 1))
			cursor.execute(f"insert into {table} {columns} values ({marks})", values)

		cursor.close()


	def update(self, table: str, datos: dict, where: dict):
		self.connect()
		cursor = self.conn.cursor()

		sql = f"update {table} set "
		values = []
		for col, val in datos.items():
			if val is not None:
				sql += f"{col} = %s, "
				values.append(val)

		sql = sql.rstrip(', ')
		sql += " where "
		for col, val in where.items():
			sql += f"{col} = %s and "
			values.append(val)
	
		sql = sql.rstrip(' and ')
		cursor.execute(sql, values)
		cursor.close()

	def commit(self):
		self.conn.commit()

	def rollback():
		self.conn.rollback()