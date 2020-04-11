from flask_jwt_extended import get_jwt_claims, jwt_required
from flask_restful import Resource, reqparse
import sqlite3
import datetime


class Weight(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('weight',
                        type=float,
                        required=True,
                        help="This field cannot be left blank",
                        )

    @jwt_required
    def post(self):
        args = Weight.parser.parse_args()
        user_weight = args['weight']
        username = get_jwt_claims()['username']
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        try:
            query = "INSERT INTO user_data VALUES(NULL,?,?,?)"
            cursor.execute(query, (username, datetime.datetime.today(), user_weight))
            connection.commit()
            connection.close()
            return {"message": "weight stored successfully"}, 201
        except:
            return {"message": "internal server error"}, 501

    @classmethod
    def get_weight(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM user_data WHERE username =? ORDER BY date DESC LIMIT 1"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        connection.close()
        return row[3]
