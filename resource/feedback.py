from flask_jwt_extended import get_jwt_claims, jwt_required
from flask_restful import Resource, reqparse
import sqlite3
import datetime


class Feedback(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('effort_score',
                        type=int,
                        required=True,
                        help="This field cannot be left blank",
                        choices=(1, 2, 3, 4, 5)
                        )

    @jwt_required
    def post(self):
        args = Feedback.parser.parse_args()
        effort_score = args['effort_score']
        username = get_jwt_claims()['username']
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        try:
            query = "INSERT INTO feedback VALUES(NULL,?,?,?)"
            cursor.execute(query, (effort_score, username, datetime.datetime.now()))
            return {"message": "feedback stored successfully"}, 201
        except:
            return {"message": "internal server error"}, 501
        connection.commit()
        connection.close()
