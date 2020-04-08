from flask import Flask, jsonify, request
import json
from flask_restful import Resource, Api
from resource.exercise import Exercise
from flask_mail import Mail, Message
from resource.encode import encode_audio, decode_audio_write_file

app = Flask(__name__)
api = Api(app)

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


api.add_resource(Exercise, '/exercise')


@app.route('/exercise_level', methods=['GET'])
def get_exercise_level():
    try:
        base64String = encode_audio('./assets/Ask_exercise_level.mp3')
    except:
        return jsonify({"message": "encoding failed"}), 500
    return jsonify({"exercise_level": str(base64String)}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
