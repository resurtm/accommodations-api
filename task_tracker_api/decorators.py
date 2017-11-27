import functools

from flask import request, make_response, jsonify
from flask.views import MethodView

from task_tracker_api.tools import validate_json


def jsonified(wrapped):
    @functools.wraps(wrapped)
    def decorator(*args, **kwargs):
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

    return decorator


def validate_data(schema, err='Unable to validate incoming data'):
    def decorator(wrapped):
        @functools.wraps(wrapped)
        def wrapper(data, *args, **kwargs):
            if not validate_json(data, schema):
                return err, 400
            return wrapped(data, *args, **kwargs)

        return wrapper

    return decorator
