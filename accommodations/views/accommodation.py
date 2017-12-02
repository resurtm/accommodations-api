from flask import request
from flask.views import MethodView

import accommodations.repos.accommodation as Accommodation
from accommodations.decorators import jsonified, jwt_auth, validate_data
from accommodations.main import app
from accommodations.tools import prepare_data


class AccommodationAPI(MethodView):
    @jwt_auth(need_user=True)
    @jsonified
    @validate_data('accommodation', 'Accommodation data is invalid')
    def post(self, json, user):
        return 'Accommodation added', {'id': Accommodation.insert(user, json)}

    @jwt_auth(need_user=True)
    @jsonified
    def get(self, user, id):
        return self.get_all(user) if id is None else self.get_one(user, id)

    def get_all(self, user):
        limit = request.args.get('limit', 10, int)
        docs = Accommodation.find_all(
            user,
            request.args.get('before', type=str),
            request.args.get('after', type=str),
            limit,
            request.args.get('order_by', type=str),
        )
        if len(docs) == 0:
            return 'No accommodations found', 404
        return '{} accommodations fetched'.format(len(docs)), \
               {'docs': prepare_data([doc for doc in docs])}

    def get_one(self, user, id):
        doc = Accommodation.find_one(user, id)
        if not doc:
            return 'Accommodation not found', 404
        return '1 accommodation fetched', \
               {'doc': prepare_data(doc)}

    @jwt_auth(need_user=True)
    @jsonified
    @validate_data('accommodation', 'Accommodation data is invalid')
    def put(self, json, user, id):
        Accommodation.update(user, id, json)
        return 'Accommodation updated'

    @jwt_auth(need_user=True)
    @jsonified
    def delete(self, _, user, id):
        Accommodation.delete(user, id)
        return 'Accommodation deleted'


view = AccommodationAPI.as_view('project_api')
app.add_url_rule('/v1/accommodation', view_func=view, methods=['POST'])
app.add_url_rule('/v1/accommodation', defaults={'id': None},
                 view_func=view, methods=['GET'])
app.add_url_rule('/v1/accommodation/<id>', view_func=view,
                 methods=['GET', 'PUT', 'DELETE'])
