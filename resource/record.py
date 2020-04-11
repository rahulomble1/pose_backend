from flask_jwt_extended import get_jwt_claims, jwt_required
from flask_restful import Resource, reqparse
import sqlite3
import datetime


class Record(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_time',
                        type=int,
                        required=True,
                        help="This field cannot be left blank",
                        )

    parser.add_argument('total_time',
                        type=int,
                        required=True,
                        help="This field cannot be left blank",
                        )

    parser.add_argument('exercise_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank",
                        )

    @jwt_required
    def post(self):
        args = Record.parser.parse_args()
        user_time = args['user_time']
        total_time = args['total_time']
        exercise_id = args['exercise_id']
        username = get_jwt_claims()['username']
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        try:
            query = "INSERT INTO exercise_record VALUES(NULL,?,?,?,?,?)"
            cursor.execute(query, (username, datetime.datetime.today(), exercise_id, user_time, total_time))
            print("#######")
            connection.commit()
            connection.close()
            return {"message": "user exercise data stored successfully"}, 201
        except:
            return {"message": "internal server error"}, 501

    @jwt_required
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        username = get_jwt_claims()['username']
        try:
            query = "SELECT * FROM exercise_record WHERE username =? ORDER BY date DESC limit 1"
            result = cursor.execute(query, (username,))
            record_list = []
            for row in result.fetchall():
                record = {"id": row[0],
                          "username": row[1],
                          "date": row[2],
                          "exercise_id": row[3],
                          "user_time": row[4],
                          "total_time": row[5]}
                record_list.append(record)
                connection.close()
            return {"record": record_list}, 200
        except:
            return {"message": "internal server error"}, 501
