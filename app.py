import datetime
from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resource.calorie import Calorie
from resource.exercise import Exercise, ExerciseRegister, Capture
from flask_mail import Mail, Message
from resource.feedback import Feedback
from resource.record import WeightRecord, CalorieRecord, Reward
from resource.user import UserRegister
from resource.voice import Voice
from resource.weight import Weight
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from resource.user import User

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'physio'

jwt = JWTManager(app)

with open('resource/config.json', 'r') as file:
    params = json.load(file)['params']

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": params["username"],
    "MAIL_PASSWORD": params["password"],

}

app.config.update(mail_settings)
mail = Mail(app)
mail.init_app(app)


@app.route('/email', methods=['POST'])
def sent_email():
    data = request.get_json()
    subject = "Hi {} {}".format(data["name"], params["subject"])
    msg = Message(subject,
                  sender=params["username"],
                  recipients=[data['email_id']],
                  body=params["body"])

    mail.send(msg)
    return jsonify({"message": "Email has been send"})


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
            expires = datetime.timedelta(days=365)
            ret = {'access_token': create_access_token(user.username, expires_delta=expires), "code": 200}
            return ret, 200
        return {"message": "please check the credentials", "code": 401}, 401

    @jwt.user_claims_loader
    def add_claims_to_access_token(self):
        args = Login.parser.parse_args()
        user = User.find_by_username(args['username'])
        return {'username': user.username,
                'age': user.age}


api.add_resource(Exercise, '/exercise')
api.add_resource(Capture, '/capture')
api.add_resource(Feedback, '/feedback')
api.add_resource(ExerciseRegister, '/exercise_register')
api.add_resource(UserRegister, '/register')
api.add_resource(Login, '/login')
api.add_resource(Calorie, '/calorie')
api.add_resource(Voice, '/voice')
api.add_resource(WeightRecord, '/weight_record')
api.add_resource(CalorieRecord, '/calorie_record')
api.add_resource(Weight, '/weight')
api.add_resource(Reward, '/reward')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
