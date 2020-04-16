from flask_jwt_extended import get_jwt_claims, jwt_required
from flask_restful import Resource, reqparse
import sqlite3
import datetime


class Feedback(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('effort_score',
                        type=str,
                        required=True,
                        help="This field cannot be left blank",
                        choices=("0", "1", "2", "3", "4", "5")
                        )

    parser.add_argument('exercise_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank",
                        )

    @jwt_required
    def post(self):
        args = Feedback.parser.parse_args()
        effort_score = args['effort_score']
        exercise_id = args['exercise_id']
        username = get_jwt_claims()['username']
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        try:
            query = "INSERT INTO feedback VALUES(NULL,?,?,?,?)"
            cursor.execute(query, (effort_score, username, datetime.datetime.today(), exercise_id))
            connection.commit()
            connection.close()
            return {"message": "feedback stored successfully", "code": 201}, 201
        except:
            return {"message": "internal server error", "code": 501}, 501

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        try:
            query = "SELECT * FROM feedback"
            result = cursor.execute(query)
            feedback_list = []
            for row in result.fetchall():
                feedback = {"id": row[0],
                            "effort_score": row[1],
                            "username": row[2],
                            "date": row[3],
                            "exercise_id": row[4]}
                feedback_list.append(feedback)
                connection.close()
            return {"feedback": feedback_list}, 200
        except:
            return {"message": "internal server error"}, 501
