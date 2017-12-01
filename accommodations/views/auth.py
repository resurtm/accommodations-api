import datetime

import bcrypt
import jwt

from accommodations.decorators import jsonified, validate_data
from accommodations.main import app
from accommodations.repos.user import user_exists, upsert_user, find_user


@app.route('/v1/auth/signup', methods=['POST'])
@jsonified
@validate_data('signup', 'Sign up data is invalid')
def signup(json):
    if user_exists(json['username'], json['email']):
        return 'User already exists', 400
    json['password'] = bcrypt.hashpw(json['password'].encode('utf-8'),
                                     bcrypt.gensalt())
    upsert_user(json['username'], json['email'])
    return 'User created'


@app.route('/v1/auth/signin', methods=['POST'])
@jsonified
@validate_data('signin', 'Sign in data is invalid')
def signin(json):
    user = find_user(json['username'], json['email'])
    if not user:
        return 'Unable to find user for sign in', 400
    if not bcrypt.checkpw(json['password'].encode('utf-8'), user['password']):
        return 'Invalid password provided', 400
    token = jwt.encode(
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=4),
         'username': user['username'],
         'email': user['email']},
        app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
    return 'Signed in successfully', {'token': token.decode('utf-8')}


@app.route('/v1/auth/check', methods=['POST'])
@jsonified
def check(json):
    if 'token' not in json:
        return 'Unable to validate auth check data', 400
    try:
        data = jwt.decode(json['token'],
                          app.config['JWT_SECRET_KEY'],
                          algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return 'Invalid token has been specified', 400
    if not user_exists(data['username'], data['email'], strict=True):
        return 'Invalid token has been specified', 400
    return 'Auth token is valid'