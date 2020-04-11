from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restful import Resource, reqparse
from resource.encode import decode_audio_write_file
from resource.speech import speech_to_text
from resource.user import User
from resource.weight import Weight


class Calorie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('time',
                        type=int,
                        required=True,
                        help="This field cannot be left empty")

    @jwt_required
    def post(self):

        args = Calorie.parser.parse_args()
        username = get_jwt_claims()['username']
        weight = Weight.get_weight(username)
        print("Weight #######", weight)
        intensity = "basic low"

        MET_vector = {"basic low": 3, "intermediate medium": 6, "advanced high": 8}
        t_min = args['time'] / 60

        try:
            MET = MET_vector.get(intensity, 2)
            wt_kg = weight
            calorie_burn = (t_min * MET * 3.5 * wt_kg) / 200
        except:
            return {"message": "Failed"}, 500
        healthpoints = int(calorie_burn/10) * 5
        return {"calorie_burn": calorie_burn, "healthpoints": healthpoints}

