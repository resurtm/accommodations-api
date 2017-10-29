import json

from flask import abort

from task_tracker_api.main import app
from task_tracker_api.tools import parse_request_json, validate_json_schema


@app.route('/v1/register', methods=['POST'])
def register():
    data = parse_request_json()
    if not validate_json_schema(data, 'user'):
        abort(400)

    # mongo.db.users.insert
    return json.dumps(data, indent=4)
