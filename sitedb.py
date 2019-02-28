from flask import Flask 
import pymongo 
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client['wp2']         #    use wp2

userTable = db['user'] 

userTable.remove()
#userTable.insert({'email': "kevin" , 'pass': None} )


#query = {"email": "mykey"}
#newVal = {"$set": {"key": "KKKK"}}  
#userTable.update_one(query, newVal)
