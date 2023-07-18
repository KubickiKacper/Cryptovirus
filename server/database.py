import pymongo
from pymongo import MongoClient
from datetime import datetime

def connection():
    CONNECTION_STRING = "mongodb://user:password@ip:port/db"
    client = MongoClient(CONNECTION_STRING)

    db = client.keys_db
    collection = db.keys    

    return client, collection

def freshInsert(private_key,public_key):
    client, collection = connection()

    data={'private_key' : private_key, 'public_key' : public_key, 'isAvailable':0, 'date' : datetime.utcnow(), 'BTCAddress' : ''}

    collection.insert_one(data)

