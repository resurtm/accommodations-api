import functools

import accommodations.repos.user as User
import accommodations.repos.bl_token as BlToken
import jwt
from accommodations.main import app
from accommodations.tools import validate_json
from flask import request, make_response, jsonify
from flask.views import MethodView


def jwt_auth(need_user=False, need_token=False):
    def decorator(wrapped):
        @functools.wraps(wrapped)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('bearer '):
                return jsonify({'data': {}, 'ok': False,
                                'msg': 'Authentication required'}), 401

            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'data': {}, 'ok': False,
                                'msg': 'Bearer token malformed'}), 401

            if BlToken.exists(token):
                return jsonify({'data': {}, 'ok': False,
                                'msg': 'Auth token has been blacklisted'}), 401

            try:
                data = jwt.decode(token,
                                  app.config['JWT_SECRET_KEY'],
                                  algorithms=['HS256'])
            except jwt.exceptions.DecodeError:
                return jsonify({'data': {}, 'ok': False,
                                'msg': 'Invalid bearer token'}), 401

            if need_user:
                user = User.find(data['email'], data['username'])
                if not user:
                    return jsonify({'data': {}, 'ok': False,
                                    'msg': 'Invalid bearer token'}), 401
                kwargs['user'] = user
            else:
                if User.exists(data['username'], data['email']):
                    return jsonify({'data': {}, 'ok': False,
                                    'msg': 'Invalid bearer token'}), 401

            if need_token:
                kwargs['token'] = token

            return wrapped(*args, **kwargs)

        return wrapper

    return decorator


def jsonified(wrapped):
    @functools.wraps(wrapped)
    def wrapper(*args, **kwargs):
        if request.is_json or request.method == 'GET':
            self = None
            if len(args) > 0 and isinstance(args[0], MethodView):
                tmp = list(args)
                self = tmp.pop(0)
                args = tuple(tmp)

            tmp = list(args)
            if request.method != 'GET':
                tmp.insert(0, request.get_json(silent=True))
            if self is not None:
                tmp.insert(0, self)
            args = tuple(tmp)

            fn_res = wrapped(*args, **kwargs)
            if type(fn_res) is not tuple:
                fn_res = (fn_res,)

            ok, msg, status, data = True, '', 200, {}
            has_ok = False
            for item in fn_res:
                t = type(item)
                if t is bool:
                    ok = item
                    has_ok = True
                elif t is str:
                    msg = item
                elif t is int:
                    status = item
                elif t is dict:
                    data = item
            if not has_ok and status != 200:
                ok = False
        else:
            ok, msg, status, data = False, 'JSON data expected', 400, {}

        resp = make_response(jsonify({'ok': ok,
                                      'msg': msg,
                                      'data': data}), status)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    return wrapper


def validate_data(schema, err='Unable to validate incoming data'):
    def decorator(wrapped):
        @functools.wraps(wrapped)
        def wrapper(*args, **kwargs):
            data = args[1] if isinstance(args[0], MethodView) else args[0]
            if not validate_json(data, schema):
                return err, 400
            return wrapped(*args, **kwargs)

        return wrapper

    return decorator
