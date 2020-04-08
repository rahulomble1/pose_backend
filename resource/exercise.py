from flask import request
from flask_restful import Resource, reqparse
from resource.encode import decode_audio_write_file
from resource.speech import speech_to_text
import sqlite3

exercise_list = [
    {
        "name": "Glute bridge",
        "description": "Exercise to strengthen hips and butt",
        "slug": "glute-bridge",
        "category": "Orthopedics"
    },
    {
        "name": "Clamshell",
        "description": "Exercise will strengthen your hips and thighs",
        "slug": "clamshell",
        "category": "Orthopedics"
    },
    {
        "name": "External rotation with elastic",
        "description": "Exercise to strengthen your arms",
        "slug": "external-rotation-with-elastic",
        "category": "Orthopedics"
    },
    {
        "name": "Putty grip",
        "description": "Exercise to maintain hand strength",
        "slug": "putty-grip",
        "category": "Hand Therapy"
    },
    {
        "name": "Putty role and pinch",
        "description": "Exercise to enhance finger strength",
        "slug": "putty-role-and-pinch",
        "category": "Hand Therapy"
    },
    {
        "name": "Ladder fast feet",
        "description": "Exercise to warm up whole body",
        "slug": "ladder-fast-feet",
        "category": "Amputee"
    },
    {
        "name": "Shoulder Exercise",
        "description": "Exercise to build strength for shoulders",
        "slug": "shoulder",
        "category": "Orthopedics"
    },
    {
        "name": "Lower Back Exercise",
        "description": "Exercise to build strength for lower back",
        "slug": "Bridges",
        "category": "Orthopedics"
    }
]


class Exercise(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('exercise_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('exercise_type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('intensity',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('duration',
                        type=int,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('source',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def post(self):
        args = Exercise.parser.parse_args()
        # data = request.get_json()

        exercise = {"exercise_name": args['exercise_name'],
                    "exercise_type": args['exercise_type'],
                    "intensity": args['intensity'],
                    "duration": args['duration'],
                    "source": args['source']}
        try:
            self.insert(exercise)
        except:
            return {'message': 'An error occurred inserting the item'}, 500  # internal server error

        return exercise, 201

    @classmethod
    def insert(cls, exercise):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO exercise VALUES (NULL,?,?,?,?,?)"
        cursor.execute(query, (
            exercise['exercise_name'], exercise['exercise_type'], exercise['intensity'], exercise['duration'],
            exercise['source']))
        connection.commit()
        connection.close()

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM exercise"
        result = cursor.execute(query)
        Exercises = []

        for row in result.fetchall():
            exercise = {"_id": row[0], "exercise_name": row[1], "exercise_type": row[2], "intensity": row[3],
                        "duration": row[4], "source": row[5]}
            Exercises.append(exercise)
        connection.close()
        return {"Exercises": Exercises}, 200

    @classmethod
    def senior_excercise(cls):
        print('#######', 'here')
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM exercise WHERE exercise_type=?"
        result = cursor.execute(query, ('senior citizen',))

        Exercises = []

        for row in result.fetchall():
            exercise = {"_id": row[0], "exercise_name": row[1], "exercise_type": row[2], "intensity": row[3],
                        "duration": row[4], "source": row[5]}
            Exercises.append(exercise)
        connection.close()
        return Exercises

    @classmethod
    def youth_excercise(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM exercise WHERE exercise_type=?"
        result = cursor.execute(query, ('youth citizen',))
        Exercises = []

        for row in result.fetchall():
            exercise = {"_id": row[0], "exercise_name": row[1], "exercise_type": row[2], "intensity": row[3],
                        "duration": row[4], "source": row[5]}
            Exercises.append(exercise)
        connection.close()
        return Exercises


