from flask import Flask 
import pymongo 
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.wp2 # use wp2


userTable = db['user'] # 

userTable.remove()