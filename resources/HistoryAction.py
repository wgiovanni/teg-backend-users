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
            result = self.queryAll("""SELECT * FROM history_action""")
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
            self.insert('HISTORY_ACTION', result)
            #result = self.queryOne("SELECT TOP 1 * FROM USER ORDER BY ID DESC")
            result = self.queryOne("SELECT * FROM HISTORY_ACTION ORDER BY ID DESC LIMIT 1")
            result['date'] = result['date'].strftime('%Y-%m-%d %H:%M:%S')
            self.commit()
        except DatabaseError as e:
            self.rollback()
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))

        return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }	

class HistoryAction(Resource):
    representations = {'application/json': make_response}

    def get(self, historyActionId):
        try:
            result = self.queryOne(dedent("""\
            SELECT * FROM HISTORY_ACTION
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
            self.update('HISTORY_ACTION', result, {'ID': historyActionId})
            result = self.queryOne("SELECT * FROM HISTORY_ACTION WHERE ID = %s", [historyActionId])
            if result is None:
                abort(404, message="Resource {} doesn't exist".format(user_id))
            self.commit()
        except DatabaseError as e:
            self.rollback()
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))

        return json.dumps(result), 201, { 'Access-Control-Allow-Origin': '*' }


    def delete(self, historyActionId):
        try:
            result = self.queryOne("SELECT * FROM HISTORY_ACTION WHERE ID = %s", [historyActionId])
            if result is None:
                abort(404, message="Resource {} doesn't exists".format(historyActionId))
            else:
                self.remove("DELETE FROM HISTORY_ACTION WHERE ID = %s", [historyActionId])
                self.commit()
        except DatabaseError as e:
            self.rollback()
            abort(500, message="{0}: {1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(404, message="Resource {} doesn't exists".format(historyActionId))

        return json.dumps(result), 204, { 'Access-Control-Allow-Origin': '*' }


	