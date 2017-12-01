import json

from accommodations.main import mongo
from accommodations.tools import JSONEncoder


def project_exists(title, owner):
    return 0 != mongo.db.project.count({
        '$and': [
            {'title': title},
            {'owners': {
                '$all': [owner],
            }},
        ],
    })


def upsert_project(title, owner):
    res = mongo.db.project.update_one(
        {
            '$and': [
                {'title': title},
                {'owners': {
                    '$all': [owner],
                }},
            ],
        },
        {
            '$setOnInsert': {
                'title': title,
                'owners': [owner],
            },
        },
        upsert=True,
    )
    project = mongo.db.project.find_one({'_id': res.upserted_id})
    return json.loads(JSONEncoder().encode(project))
