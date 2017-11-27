from task_tracker_api.main import mongo


def _user_exists_query(username, email):
    query = {'$or': []}
    if username is not None:
        query['$or'].append({'username': username})
    if email is not None:
        query['$or'].append({'email': email})
    if len(query['$or']) == 0:
        raise ValueError('At least one conditional argument must be passed')
    return query


def user_exists(username=None, email=None):
    query = _user_exists_query(username=username, email=email)
    return 0 != mongo.db.users.count(query)


def upsert_user(username=None, email=None, data_on_insert=None, data=None):
    payload = {}
    if data is not None:
        payload['$set'] = data
    if data_on_insert is not None:
        payload['$setOnInsert'] = data_on_insert
    if len(payload) == 0:
        raise ValueError('At least one data argument must be passed')
    query = _user_exists_query(username=username, email=email)
    print(mongo.db.users.update_one(query, payload, upsert=True))
