from flask_restful import Resource, reqparse
from resource.encode import decode_audio_write_file
from resource.speech import speech_to_text
from resource.user import User
from resource.session import open_and_load_session


class Calorie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('time',
                        type=int,
                        required=True,
                        help="This field cannot be left empty")

    def post(self):

        args = Calorie.parser.parse_args()
        params = open_and_load_session()
        weight = params['weight']
        intensity = params['intensity']

        MET_vector = {"basic low": 2, "intermediate medium": 5, "advanced high": 7}
        t_min = args['time'] / 60

        try:
            MET = MET_vector.get(intensity, 2)
            wt_kg = weight
            calorie_burn = (t_min * MET * 3.5 * wt_kg) / 200
        except:
            return {"message": "Failed"}, 500
        print("#########", calorie_burn)
        return {"calorie_burn": calorie_burn}

