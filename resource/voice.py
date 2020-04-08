from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restful import Resource, reqparse
from resource.encode import decode_audio_write_file
from resource.exercise import Exercise
from resource.speech import speech_to_text
from resource.user import User


class Voice(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('audio',
                        type=str,
                        required=True,
                        help="This field cannot be left empty")

    @jwt_required
    def post(self):

        args = Voice.parser.parse_args()
        # decode_audio_write_file(args["audio"])

        # text = speech_to_text('resource/abc.mp3')
        text = "exercise"
        print("transcribed text", text)
        if "exercise" in text:
            username = get_jwt_claims()['username']
            user = User.find_by_username(username)

            try:
                if user and user.age > 45:
                    exercise_list = Exercise.senior_excercise()
                    return {"Exercise": exercise_list}, 200
                elif user and user.age < 45:
                    exercise_list = Exercise.youth_excercise()
                    return {"Exercise": exercise_list}, 200
            except:
                return {"message": 'internal server error'}, 501

        elif "yoga" in text:
            return {"message": "Sorry, no yoga listed for now"}, 404
        elif "Tai" or "chi" in text:
            return {"message": "Sorry, no tai chi listed for now"}, 404
