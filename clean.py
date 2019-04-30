from flask import Flask 
import pymongo 
from pymongo import MongoClient
from bson.objectid import ObjectId

def clearMe():
   client = MongoClient('130.245.170.76', 27017)
   db = client['stack']         #    use wp2

   userTable = db['user'] 
   answerTable = db['answer']
   questionTable = db['question']
   ipTable = db['ip']
   upvoteTable = db['upvote']
   mediaTable = db['mediaID']

   userTable.drop()
   answerTable.drop()
   questionTable.drop()
   ipTable.drop() 
   upvoteTable.drop()
   mediaTable.drop()

   userTable = db['user'] 
   answerTable = db['answer']
   questionTable = db['question']
   ipTable = db['ip']
   upvoteTable = db['upvote']
   mediaTable = db['mediaID']


   userTable.insert({})
   answerTable.insert({})
   questionTable.insert({})
   ipTable.insert({})
   upvoteTable.insert({})
   mediaTable.insert({})

   userTable.delete_many({})
   answerTable.delete_many({})
   questionTable.delete_many({})
   ipTable.delete_many({})
   upvoteTable.delete_many({})
   mediaTable.delete_many({})
   print('UPDATED DATA')



def connectM():
   client = MongoClient('130.245.170.76', 27017)
   db = client['stack']  
   questionTable = db['question'].find()
   for q in questionTable:
      print(q['title'])
      break

# from cassandra.cluster import Cluster
# cluster = Cluster()
# cassSession = cluster.connect(keyspace='hw5')


# query = "SELECT count(*) FROM imgs WHERE fileID = '" + 'DR5SW9DWY8GUXCEI4EKNW130YGCK3XAQF9JOA41X' + "';"
# row = cassSession.execute(query)[0].count

# print(row)