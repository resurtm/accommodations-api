import functools

import jwt
from flask import request, make_response, jsonify
from flask.views import MethodView

from task_tracker_api.main import app
from task_tracker_api.repos.user import find_user, user_exists
from task_tracker_api.tools import validate_json


def jwt_auth(need_user=False):
    def decorator(wrapped):
        @functools.wraps(wrapped)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('bearer '):
                return jsonify({'ok': False,
                                'msg': 'Authentication required'}), 401

            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'ok': False,
                                'msg': 'Bearer token malformed'}), 401

            try:
                data = jwt.decode(token,
                                  app.config['JWT_SECRET_KEY'],
                                  algorithms=['HS256'])
            except jwt.exceptions.DecodeError:
                return jsonify({'ok': False,
                                'msg': 'Invalid bearer token'}), 401

            if need_user:
                user = find_user(data['username'], data['email'])
                if not user:
                    return jsonify({'ok': False,
                                    'msg': 'Invalid bearer token'}), 401
                kwargs['user'] = user
            else:
                if user_exists(data['username'], data['email'], true):
                    return jsonify({'ok': False,
                                    'msg': 'Invalid bearer token'}), 401

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
                tmp.insert(0, request.json)
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
                                      **data}), status)
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
