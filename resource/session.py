import json


def open_and_load_session():
    with open('assets/session.json', 'r') as file:
        params = json.load(file)['params']
        return params


def writeSession(params):
    with open('assets/session.json', 'w') as file:
        file.write(json.dumps({"params": params}))


def username_weight(value="", weight_val=0):
    params = open_and_load_session()
    params['username'] = value
    params['weight'] = weight_val
    writeSession(params)


def intensity_exercise_type(value="", type=""):
    params = open_and_load_session()
    params['intensity'] = value.lower()
    params['exercise_type'] = type.lower()
    writeSession(params)

