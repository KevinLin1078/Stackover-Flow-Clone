from flask import Flask 
import pymongo 
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.test_database
collection = db['test_database']
import datetime

import pprint
from pprint import pprint

post = {
	"author": "mike",
	"date": datetime.datetime.utcnow()
}
db.posts.insert(post)
db.collection.find() 
cursor = collection.find({})
for document in cursor: 
    print(document)

print ( "hello world" )
