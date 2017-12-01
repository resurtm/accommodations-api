from accommodations.main import mongo


def exists(username, email):
    return 0 != mongo.db.users.count({
        '$or': [
            {'username': username},
            {'email': email},
        ],
    })


def upsert(data):
    res = mongo.db.users.update_one(
        {'$or': [
            {'username': data['username']},
            {'email': data['email']},
        ]},
        {'$setOnInsert': {
            'username': data['username'],
            'email': data['email'],
            'password': data['password'],
        }},
        upsert=True,
    )
    return mongo.db.users.find_one({'_id': res.upserted_id})


def find_by_email(email):
    return mongo.db.users.find_one({'email': email})
