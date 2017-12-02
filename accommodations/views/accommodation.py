import json

from flask import request
from flask.views import MethodView

import accommodations.repos.accommodation as Accommodation
from accommodations.decorators import jsonified, jwt_auth, validate_data
from accommodations.main import app
from accommodations.tools import JSONEncoder


class AccommodationAPI(MethodView):
    @jwt_auth(need_user=True)
    @jsonified
    @validate_data('accommodation', 'Accommodation data is invalid')
    def post(self, json, user):
        return {'id': Accommodation.insert(user, json)}

    def get_all(self, user):
        limit = request.args.get('limit', 10, int)
        docs = Accommodation.find_all(
            user,
            request.args.get('before', type=str),
            request.args.get('after', type=str),
            limit,
            request.args.get('order_by', type=str),
        )
        return '{} accommodations fetched'.format(limit), {
            'docs': json.loads(JSONEncoder().encode([doc for doc in docs]))
        }

    def get_one(self, user, id):
        doc = Accommodation.find_one(user, id)
        return '1 accommodation fetched', {
            'doc': json.loads(JSONEncoder().encode(doc))
        }

    @jwt_auth()
    @jsonified
    def put(self, json, id):
        return {'data': json, 'method': 'update project {}'.format(str(id))}

    @jwt_auth()
    @jsonified
    def delete(self, json, id):
        return {'data': json, 'method': 'delete project {}'.format(str(id))}

    @jwt_auth(need_user=True)
    @jsonified
    def get(self, user, id):
        return self.get_all(user) if id is None else self.get_one(user, id)


view = AccommodationAPI.as_view('project_api')
app.add_url_rule('/v1/accommodation', view_func=view, methods=['POST'])
app.add_url_rule('/v1/accommodation', defaults={'id': None},
                 view_func=view, methods=['GET'])
app.add_url_rule('/v1/accommodation/<id>', view_func=view,
                 methods=['GET', 'PUT', 'DELETE'])
