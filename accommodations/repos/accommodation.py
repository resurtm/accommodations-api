import datetime

import pymongo
from bson.objectid import ObjectId

from accommodations.main import mongo


def insert(owner, doc):
    owner = owner if isinstance(owner, ObjectId) else owner['_id']
    doc = {'title': doc['title'],
           'description': doc.get('description', ''),
           'owners': [owner],
           'created_at': datetime.datetime.utcnow(),
           'updated_at': datetime.datetime.utcnow()}
    res = mongo.db.accommodations.insert_one(doc)
    return str(res.inserted_id)


def find_all(owner, before=None, after=None, limit=10, order_by='updated_at'):
    filter = {'$and': [
        {'owners': {'$all': [
            owner if isinstance(owner, ObjectId) else owner['_id'],
        ]}},
    ]}
    if before is not None:
        filter['$and'].append({'_id': {'$lte': ObjectId(before)}})
    if after is not None:
        filter['$and'].append({'_id': {'$gte': ObjectId(after)}})

    return mongo.db.accommodations.find(**{
        'filter': filter,
        'limit': limit,
        'sort': [(
            order_by[1:]
            if order_by[0] == '-' or order_by[0] == '+' else
            order_by,
            pymongo.DESCENDING if order_by[0] == '-' else pymongo.ASCENDING,
        )],
    })
