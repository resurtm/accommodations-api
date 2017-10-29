import datetime

import bcrypt
import jwt
from flask import abort, jsonify

from task_tracker_api.main import app, mongo
from task_tracker_api.tools import parse_request_json, validate_json_schema


@app.route('/v1/register', methods=['POST'])
def register():
    data = parse_request_json()
    if not validate_json_schema(data, 'user'):
        abort(400)

    count = mongo.db.users.count({
        '$or': [
            {'username': data['username']},
            {'email': data['email']},
        ],
    })
    if count != 0:
        abort(400)

    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'),
                                     bcrypt.gensalt())
    mongo.db.users.insert_one(data)
    return jsonify({})


@app.route('/v1/auth', methods=['POST'])
def auth():
    data = parse_request_json()
    if not validate_json_schema(data, 'auth'):
        abort(400)

    user = mongo.db.users.find_one({'username': data['username']})
    if not user:
        abort(400)

    if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        abort(400)

    token = jwt.encode(
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=4),
         'username': user['username'], 'email': user['email']},
        app.config['JWT_SECRET_KEY']
    )

    return jsonify({'token': token.decode('utf-8')})


@app.route('/v1/check', methods=['POST'])
def check():
    data = parse_request_json()
    if 'token' not in data:
        abort(400)

    data = jwt.decode(data['token'], app.config['JWT_SECRET_KEY'],
                      algorithms=['HS256'])

    count = mongo.db.users.count({
        '$and': [
            {'username': data['username']},
            {'email': data['email']},
        ],
    })
    if count == 0:
        abort(400)

    return jsonify({})
