import json
from os import path as p

import jsonschema
from bson import ObjectId

from task_tracker_api.main import app


def validate_json(data, schema):
    path = p.join(app.config['JSON_SCHEMA_PATH'], schema + '.json')
    with open(path, 'r') as fp:
        fd = json.loads(fp.read())
    try:
        jsonschema.validate(data, fd)
    except jsonschema.ValidationError:
        return False
    return True


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
