import pymysql
#import psycopg2
import configparser

class BD:
	conn = None

	def connect(self):
		"""Consulta las propiedades de conexión del archivo user.properties en la sección [DB]
        y crea la conexión a la base de datos. Esto se realiza una sola vez por cada instancia de la clase."""
		if self.conn is None:
			config = configparser.ConfigParser()
			if not config.read('user.properties'):
				raise Exception ('Error leyendo el archivo user.properties')

			#print(config["BD"])
			#self.conn = psycopg2.connect(config["BD"]["connstring"])
			self.conn = pymysql.connect(host='localhost', user='root', password='', db='prueba')
			#self.conn = psycopg2.connect(host="localhost", database="prueba", user="postgres", password="123456")

	def queryAll(self, sql: str, params: list=[], columns: list=None):
		"""
        Ejecuta una consulta a la base de datos y devuelve todos los registros.

        :param sql: Comando SELECT a ejecutar.
        :param params: Lista de parámetros para asociar al comando SELECT.
        :param columns: Lista opcional de nombres de columnas para los registros consultados.\n
            Si no se especifica este parámetro los registros se devuelven con los nombres de columnas retornados por
            la consulta ejecutada.
        :return: Retorna una lista de diccionarios con los datos de cada registro retornado por la consulta ejecutada.\n
            Ej. [{"id": 1, "first_name": "Jose", ...}, ...]
        """
		self.connect()
		cursor = self.conn.cursor()
		cursor.execute(sql, params)
		rows = cursor.fetchall()
	
		if columns is None:
			columns = [column[0].lower() for column in cursor.description]
		cursor.close()
		return [dict(zip(columns, row)) for row in rows]

	def queryOne(self, sql: str, params: list=[], columns: list=None):
		"""
        Ejecuta una consulta a la base de datos y devuelve el primer registro.

        :param sql: Comando SELECT a ejecutar.
        :param params: Lista de parámetros para asociar al comando SELECT.
        :param columns: Lista opcional de nombres de columnas para los registros consultados.\n
            Si no se especifica este parámetro los registros se devuelven con los nombres de columnas retornados por
            la consulta ejecutada.
        :return: Retorna un diccionario con los datos del primer registro retornado por la consulta ejecutada.\n
            Ej. {"id": 1, "first_name": "Jose", ...}
        """
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
		"""
        Inserta uno o varios registros en una tabla.

        :param table: Nombre de la tabla.
        :param datos: Diccionario con las keys para los nombres de columnas y los valores para insertar.\n
            Ej. {"id": 1, "first_name": "Jose", ...}\n
            Este diccionario sobreescribe los valores de los parámetros columns y values.
        :param columns: Columnas de la tabla donde se van a insertar los datos.\n
            Puede ser un string separado por comas. ej. 'id, first_name, ...'\n
            Puede ser una lista de string. ej. ['id', 'first_name', ...]\n
        :param values: Lista de valores a insertar en la tabla.\n
            Puede ser una lista de valores simples para un solo registro. ej. [1, 'Jose', ...]\n
            Puede ser una lista de tuplas para insertar varios registros. ej. [(1, 'Jose', ...), (2, 'Jesus', ...), ...]
        """
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
			marks = "(%s" + (",%s" * (len(values[0]) - 1)) + ")"
			sql = f"insert into {table} {columns} values {marks}", values
			cursor.execute(sql, values)
		else:
			marks = "(%s" + (",%s" * (len(values) - 1)) + ")"
			sql = f"insert into {table} {columns} values {marks}"
			cursor.execute(sql, values)	
		
		cursor.close()


	def update(self, table: str, datos: dict, where: dict):
		"""
        Actualiza uno o varios registros en una tabla.

        :param table: Nombre de la tabla.
        :param datos: Diccionario con las keys para los nombres de columnas y los nuevos valores los registros.\n
            Ej. {"id": 1, "first_name": "Jose", ...}.
        :param where: Diccionario con los datos para la condición del update.\n
            Ej. {"id": 1, ...}.
        """
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

	def remove(self, sql: str, params: list):
		print("Entro")
		self.connect()
		cursor = self.conn.cursor()
		cursor.execute(sql, params)
		cursor.close()


	def commit(self):
		self.conn.commit()
		
	def rollback():
		self.conn.rollback()