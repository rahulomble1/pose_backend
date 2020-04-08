import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from resource.session import username_weight
from resource.user import User
import jwt


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def post(self):
        args = Login.parser.parse_args()
        user = User.find_by_username(args['username'])

        if user and safe_str_cmp(user.password, args['password']):
            username_weight(user.username, user.weight)
            return {"message": "login successfully"}, 200
        return {"message": "please check the credentials"}, 401
