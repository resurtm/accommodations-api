from accommodations.main import mongo


def upsert(token, user):
    res = mongo.db.bl_token.update_one(
        {'token': token},
        {'$setOnInsert': {
            'token': token,
            'user': user['_id'],
        }},
        upsert=True,
    )
    return mongo.db.bl_token.find_one({'_id': res.upserted_id})


def exists(token):
    return 0 != mongo.db.bl_token.count({'token': token})
