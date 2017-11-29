from task_tracker_api.main import mongo


def user_exists(username, email, strict=False):
    return 0 != mongo.db.users.count({
        '$and' if strict else '$or': [
            {'username': username},
            {'email': email},
        ],
    })


def upsert_user(username, email):
    res = mongo.db.users.update_one(
        {
            '$or': [
                {'username': username},
                {'email': email},
            ],
        },
        {
            '$setOnInsert': {
                'username': username,
                'email': email,
            },
        },
        upsert=True,
    )
    return mongo.db.users.find_one({'_id': res.upserted_id})


def find_user(username, email):
    return mongo.db.users.find_one({
        '$and': [
            {'username': username},
            {'email': email},
        ],
    })
