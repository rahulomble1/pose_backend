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

        try:
            decode_audio_write_file(args["audio"])
            text = speech_to_text('resource/abc.mp3')
        except:
            return {"message": "internal server error"}, 501

        # text = "exercise"
        print("transcribed text", text)
        if "exercise" in text:
            return {"message": "exercise: valid"}, 200
        elif "yoga" in text:
            return {"message": "yoga: valid"}, 200
        elif "Tai" or "chi" in text:
            return {"message": "tai chi: valid"}, 200
        else:
            return {"message": 'invalid'}, 501
