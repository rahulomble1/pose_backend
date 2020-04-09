from flask import Flask, jsonify, request
import json

from flask_jwt_extended import JWTManager
from flask_restful import Api
from resource.calorie import Calorie
from resource.exercise import Exercise, ExerciseRegister, Capture
from flask_mail import Mail, Message
from resource.encode import encode_audio
from resource.feedback import Feedback
from resource.user import UserRegister
from resource.voice import Voice


app = Flask(__name__)
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


@app.route('/efforts', methods=['GET'])
def get_efforts():
    try:
        effort = encode_audio('./assets/Great_effort.mp3')
    except:
        return jsonify({"message": "Encoding Failed"}), 500
    return jsonify({"effort": str(effort)}), 200


@app.route('/ask_exercise_level', methods=['GET'])
def get_exercise_level():
    try:
        askExe = encode_audio('./assets/Ask_exercise_level.mp3')
    except:
        return jsonify({"message": "Encoding Failed"}), 500
    return jsonify({"exercise_level": str(askExe)}), 200


@app.route('/choose_exercise', methods=['GET'])
def get_choose_exercise():
    try:
        chooseExe = encode_audio('./assets/Choose_exercise.mp3')
    except:
        return jsonify({"message": "Encoding Failed"}), 500
    return jsonify({"exercise_level": str(chooseExe)}), 200


@app.route('/exercises', methods=['GET'])
def get_exercise():
    try:
        exe = encode_audio('./assets/Okay!_Exercises.mp3')
    except:
        return jsonify({"message": "Encoding Failed"}), 500
    return jsonify({"exercise_level": str(exe)}), 200


@app.route('/how_you_feeling', methods=['GET'])
def get_how_you_feeling():
    try:
        feeling = encode_audio('./assets/How_would_you_like_to_workout_today.mp3')
    except:
        return jsonify({"message": "Encoding Failed"}), 500
    return jsonify({"feeling": str(feeling)}), 200


@app.route('/readiness', methods=['GET'])
def get_ready():
    try:
        ready = encode_audio('./assets/I_am_Ready.mp3')
    except:
        return jsonify({"message": "Encoding Failed"}), 500
    return jsonify({"exercise_level": str(ready)}), 200


from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from resource.user import User


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
            ret = {'access_token': create_access_token(user.username)}
            return ret, 200
        return {"message": "please check the credentials"}, 401

    @jwt.user_claims_loader
    def add_claims_to_access_token(self):
        args = Login.parser.parse_args()
        user = User.find_by_username(args['username'])
        return {'username': user.username,
                'weight': user.weight,
                'age': user.age}


api.add_resource(Exercise, '/exercise')
api.add_resource(Capture, '/capture')
api.add_resource(Feedback, '/feedback')
api.add_resource(ExerciseRegister, '/exercise_register')
api.add_resource(UserRegister, '/register')
api.add_resource(Login, '/login')
api.add_resource(Calorie, '/calorie')
api.add_resource(Voice, '/voice')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
