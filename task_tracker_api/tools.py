import json
import os

import jsonschema
from flask import request

from task_tracker_api.main import app


def parse_request_json():
    return json.loads(request.data.decode('utf-8', 'strict'))


def validate_json_schema(json_data, schema_name):
    path = os.path.join(app.config['JSON_SCHEMA_PATH'],
                        '{}.json'.format(schema_name))
    with open(path, 'r') as fp:
        schema_data = json.loads(fp.read())
    try:
        jsonschema.validate(json_data, schema_data)
    except jsonschema.ValidationError:
        return False
    return True
