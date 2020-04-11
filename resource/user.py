import sqlite3
import flask
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password, age, name):
        self.id = _id
        self.name = name
        self.username = username
        self.password = password
        self.age = age

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select = 'SELECT * FROM user WHERE username = ?'

        result = cursor.execute(select, (username,))
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select = 'SELECT * FROM user WHERE id = ?'

        result = cursor.execute(select, (_id,))
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        required=True,
                        type=str,
                        help='this field cannot be left empty')
    parser.add_argument('password',
                        required=True,
                        type=str,
                        help='this field cannot be left empty')
    parser.add_argument('age',
                        required=True,
                        type=int,
                        help='this field cannot be left empty')

    parser.add_argument('name',
                        required=True,
                        type=str,
                        help='this field cannot be left empty')

    def post(self):
        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        if User.find_by_username(data['username']):
            return {'message': 'The user_name {} is already exist'.format(data['username'])}, 400

        query = "INSERT INTO user VALUES (NULL,?,?,?,?)"
        try:
            cursor.execute(query, (data['username'], data['password'], data['age'], data['name']))
        except:
            return {"message": "User not created successfully"}, 501
        connection.commit()
        connection.close()

        return {"message": "User created  successfully."}, 201
