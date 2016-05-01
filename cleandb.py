import json
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.recommendation
id_collection = db.idcollection
order = db.order
buying_frequency = db.buying_frequency

id_collection.remove({})
order.remove({})
buying_frequency.remove({})
