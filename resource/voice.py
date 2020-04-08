from flask_restful import Resource, reqparse
from resource.encode import decode_audio_write_file
from resource.exercise import Exercise
from resource.speech import speech_to_text
from resource.session import open_and_load_session, intensity_exercise_type
from resource.user import User


class Voice(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('audio',
                        type=str,
                        required=True,
                        help="This field cannot be left empty")

    def post(self):

        args = Voice.parser.parse_args()
        # decode_audio_write_file(args["audio"])

        # text = speech_to_text('resource/abc.mp3')
        text = "exercise"
        print("transcribed text", text)
        if "exercise" in text:
            params = open_and_load_session()
            username = params['username']
            user = User.find_by_username(username)
            print('###########', user.age)
            try:
                if user and user.age > 45:
                    list_excercises = Exercise.senior_excercise()
                    print('###########', list_excercises)
                    intensity_exercise_type('basic low', 'senior')
                    return {"Excercise": list_excercises}, 200
                elif user and user.age < 45:
                    intensity_exercise_type('basic low', 'senior')
                    list_excercises = Exercise.youth_excercise()
                    return {"Excercise": list_excercises}, 200
            except:
                return {"message": 'internal server error'}, 501

        elif "yoga" in text:
            return {"message": "Sorry, no yoga listed for now"}, 404
        elif "Tai" or "chi" in text:
            return {"message": "Sorry, no tai chi listed for now"}, 404
