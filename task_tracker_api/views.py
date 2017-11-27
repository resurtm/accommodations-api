import datetime
import json

import bcrypt
import jwt
from flask import jsonify, request

from .main import app, mongo
from .tools import validate_json


@app.route('/v1/auth/signup', methods=['POST'])
def register():
    data = json.loads(request.data.decode('utf-8', 'strict'))
    if not validate_json(data, 'signup'):
        return jsonify({'ok': False,
                        'msg': 'Unable to validate sign up data'}), 400

    query = {'$or': [
        {'username': data['username']},
        {'email': data['email']},
    ]}
    count = mongo.db.users.count(query)
    if count != 0:
        return jsonify({'ok': False,
                        'msg': 'User already exists'}), 400

    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'),
                                     bcrypt.gensalt())
    mongo.db.users.update_one(query,
                              {"$setOnInsert": data},
                              upsert=True)
    return jsonify({'ok': True, 'msg': 'User created'})


@app.route('/v1/auth/signin', methods=['POST'])
def auth():
    data = json.loads(request.data.decode('utf-8', 'strict'))
    if not validate_json(data, 'signin'):
        return jsonify({'ok': False,
                        'msg': 'Unable to validate sign in data'}), 400

    user = mongo.db.users.find_one({'username': data['username']})
    if not user:
        return jsonify({'ok': False,
                        'msg': 'Unable to find user for sign in'}), 400
    if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({'ok': False,
                        'msg': 'Invalid password provided'}), 400
    token = jwt.encode(
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=4),
         'username': user['username'],
         'email': user['email']},
        app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
    return jsonify({'ok': True,
                    'msg': 'Signed in successfully',
                    'token': token.decode('utf-8')})


@app.route('/v1/auth/check', methods=['POST'])
def check():
    data = json.loads(request.data.decode('utf-8', 'strict'))
    if 'token' not in data:
        return jsonify({'ok': False,
                        'msg': 'Unable to validate auth check data'}), 400

    try:
        data = jwt.decode(data['token'],
                          app.config['JWT_SECRET_KEY'],
                          algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return jsonify({'ok': False,
                        'msg': 'Invalid token has been specified'}), 400

    count = mongo.db.users.count({'$and': [
        {'username': data['username']},
        {'email': data['email']},
    ]})
    if count == 0:
        return jsonify({'ok': False,
                        'msg': 'Invalid token has been specified'}), 400

    return jsonify({'ok': True,
                    'msg': 'Auth token is valid'})
