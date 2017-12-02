import datetime

import bcrypt
import jwt

import accommodations.repos.bl_token as BlToken
import accommodations.repos.user as User
from accommodations.decorators import jsonified, validate_data, jwt_auth
from accommodations.main import app


@app.route('/v1/auth/signin', methods=['POST'])
@jsonified
@validate_data('signin', 'Sign in data is invalid')
def signin(json):
    user = User.find_by_email(json['email'])
    if not user:
        return 'Unable to find user to sign in', 400
    if not bcrypt.checkpw(json['password'].encode('utf-8'), user['password']):
        return 'Invalid password has been provided', 400
    token = jwt.encode(
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=4),
         'username': user['username'],
         'email': user['email']},
        app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
    return 'Signed in successfully', {'token': token.decode('utf-8')}


@app.route('/v1/auth/signout', methods=['POST'])
@jwt_auth(need_user=True, need_token=True)
@jsonified
def signout(_, user, token):
    BlToken.upsert(token, user)
    return 'Token has been made blacklisted'


@app.route('/v1/auth/signup', methods=['POST'])
@jsonified
@validate_data('signup', 'Sign up data is invalid')
def signup(json):
    if User.exists(json['username'], json['email']):
        return 'User already exists', 400
    json['password'] = bcrypt.hashpw(json['password'].encode('utf-8'),
                                     bcrypt.gensalt())
    User.upsert(json)
    return 'User created'


@app.route('/v1/auth/check', methods=['POST'])
@jsonified
def check(json):
    if 'token' not in json:
        return 'Unable to validate auth check data', 400
    if BlToken.exists(json['token']):
        return 'Token has been blacklisted', 400
    try:
        data = jwt.decode(json['token'],
                          app.config['JWT_SECRET_KEY'],
                          algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return 'Invalid token has been specified', 400
    if not User.exists(data['username'], data['email']):
        return 'Invalid token has been specified', 400
    return 'Auth token is valid'
