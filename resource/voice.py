from flask_restful import Resource, reqparse
from resource.encode import decode_audio_write_file
from resource.speech import speech_to_text


class Voice(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('audio',
                        type=str,
                        required=True,
                        help="This field cannot be left empty")

    def post(self):

        args = Voice.parser.parse_args()
        decode_audio_write_file(args["audio"])

        text = speech_to_text('resource/abc.mp3')
        print("transcribed text", text)
        if "exercise" in text:
            pass
        elif "yoga" in text:
            pass
        elif "Tai" or "chi" in text:
            pass
