from flask_restful import abort, Resource
from flask import request
import simplejson as json
from flask import make_response
from pymysql import DatabaseError
from textwrap import dedent
from datetime import datetime
from common.BD import BD


class HistoryActionList(BD, Resource):
    representations = {'application/json': make_response}

    def get(self):
        try:
            result = self.queryAll("""SELECT * FROM history_action WHERE status = 1 ORDER BY date DESC""")
            for r in result:
                r['date'] = r['date'].strftime('%Y-%m-%d %H:%M:%S')
        except DatabaseError as e:
            self.rollback()
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))

        return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

    def post(self):
        try:
            result = request.get_json(force=True)
            print(result)
            self.insert('history_action', result)
            #result = self.queryOne("SELECT TOP 1 * FROM USER ORDER BY ID DESC")
            result = self.queryOne("SELECT * FROM history_action ORDER BY id DESC LIMIT 1")
            result['date'] = result['date'].strftime('%Y-%m-%d %H:%M:%S')
            self.commit()
        except DatabaseError as e:
            self.rollback()
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))

        return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }

    def delete(self):
        try:
            print("Entro")
            #self.remove("DELETE FROM HISTORY_ACTION",[])
            self.remove("UPDATE history_action SET status = %s",[False])
            self.commit()
            print("Salio")
        except DatabaseError as e:
            self.rollback()
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(404, message="Resource {} doesn't exists")

        return json.dumps({"message": "Eliminado todos los registros"}), 204, { 'Access-Control-Allow-Origin': '*' }	

class HistoryAction(Resource, BD):
    representations = {'application/json': make_response}

    def get(self, historyActionId):
        try:
            result = self.queryOne(dedent("""\
            SELECT * FROM history_action
            WHERE id = %s"""), [historyActionId])
            if result is None:
                abort(404, message="Resource {} doesn't exists".format(historyActionId))
        except DatabaseError as e:
            self.rollback()
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
        return json.dumps(result), 200, { 'Access-Control-Allow-Origin': '*' }

    def put(self, historyActionId):
        try:
            result = self.parser.parse_args()
            print(result)
            del result['id']
            self.update('history_action', result, {'ID': historyActionId})
            result = self.queryOne("SELECT * FROM history_action WHERE id = %s", [historyActionId])
            if result is None:
                abort(404, message="Resource {} doesn't exist".format(historyActionId))
            self.commit()
        except DatabaseError as e:
            self.rollback()
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))

        return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }



	