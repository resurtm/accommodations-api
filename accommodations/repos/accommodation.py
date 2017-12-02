import datetime

import pymongo
from bson.objectid import ObjectId

from accommodations.main import mongo


def prepare_owner(owner):
    return owner if isinstance(owner, ObjectId) else owner['_id']


def insert(owner, doc):
    doc = {'title': doc['title'],
           'description': doc.get('description', ''),
           'owners': [prepare_owner(owner)],
           'created_at': datetime.datetime.utcnow(),
           'updated_at': datetime.datetime.utcnow()}
    res = mongo.db.accommodations.insert_one(doc)
    return str(res.inserted_id)


def update(owner, id, doc):
    flt = {
        '$and': [
            {'owners': {
                '$all': [prepare_owner(owner)],
            }},
            {'_id': ObjectId(id)},
        ],
    }
    doc = {'$set': {
        'title': doc['title'],
        'description': doc.get('description', ''),
        'updated_at': datetime.datetime.utcnow(),
    }}
    res = mongo.db.accommodations.update_one(flt, doc)
    return str(res.upserted_id)


def delete(owner, id):
    mongo.db.accommodations.delete_one({
        '$and': [
            {'owners': {
                '$all': [prepare_owner(owner)],
            }},
            {'_id': ObjectId(id)},
        ],
    })


def find_all(owner, before=None, after=None, limit=10, order_by=None):
    flt = {'$and': [
        {'owners': {
            '$all': [prepare_owner(owner)],
        }},
    ]}
    if before is not None:
        flt['$and'].append({'_id': {'$lte': ObjectId(before)}})
    if after is not None:
        flt['$and'].append({'_id': {'$gte': ObjectId(after)}})
    if order_by is None:
        order_by = 'updated_at'
    res = mongo.db.accommodations.find(**{
        'filter': flt,
        'limit': limit,
        'sort': [(
            order_by[1:]
            if order_by[0] == '-' or order_by[0] == '+' else
            order_by,
            pymongo.DESCENDING if order_by[0] == '-' else pymongo.ASCENDING,
        )],
    })
    return []


def find_one(owner, id):
    return mongo.db.accommodations.find_one({
        '$and': [
            {'owners': {
                '$all': [prepare_owner(owner)],
            }},
            {'_id': ObjectId(id)},
        ],
    })
