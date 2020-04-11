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
        except:
            return {"message": "decoding internal server error"}, 501
        # try:
        text = speech_to_text('resource/abc.mp3')
        # except :
        #     return {"message": "speech to text conversion failed"}
        # text = "exercise"
        print("transcribed text", text)
        if text:
            if "exercise" in text:
                return {"text": text, "valid": True}, 200
            elif "yoga" in text:
                return {"text": text,  "valid": True}, 200
            elif "Tai" in text or "chi" in text:
                return {"text": text,  "valid": True}, 200
            return {"text": text,  "valid": False}, 501
        return {"message": "no text detected", "valid": False},  501
