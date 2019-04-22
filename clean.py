from flask import Flask 
import pymongo 
from pymongo import MongoClient


def clearMe():
   client = MongoClient()
   db = client['stack']         #    use wp2

   userTable = db['user'] 
   answerTable = db['answer']
   questionTable = db['question']
   ipTable = db['ip']
   upvoteTable = db['upvote']

   userTable.drop()
   answerTable.drop()
   questionTable.drop()
   ipTable.drop() 
   upvoteTable.drop()

   userTable = db['user'] 
   answerTable = db['answer']
   questionTable = db['question']
   ipTable = db['ip']
   upvoteTable = db['upvote']


   userTable.insert({})
   answerTable.insert({})
   questionTable.insert({})
   ipTable.insert({})
   upvoteTable.insert({})

   userTable.delete_many({})
   answerTable.delete_many({})
   questionTable.delete_many({})
   ipTable.delete_many({})
   upvoteTable.delete_many({})
   print('UPDATED DATA')

def experiment():
   client = MongoClient()
   db = client['stack']         #    use wp2
   userTable = db['user']
   from bson.objectid import ObjectId
   result = userTable.find_one({'_id': ObjectId('5cb777776954c773ae6226ff')})
   print(result)
      
# text = raw_input("Type (cleandata) or (exp)\n")
# if 'clean' in text:
#    clearMe()
#    print('Cleared Databased')
# else:
#    experiment()
#    print('Experiment successfull')



'''
query =' BRANCHes'.strip().lower()
print("WITH QUERY")
search_query = {}
search_query['$or'] = []

query_title = {}
query_title['$or'] = []

query_body = {}
query_body['$or'] =[]

query = query.split(' ')

for each in query:
   term = {}
   term['$or'] = []
   term['$or'].append({'title':{'$regex': ' ' + each}})
   term['$or'].append({'title':{'$regex': each + ' '}})
   query_title['$or'].append(term)

   term = {}
   term['$or'] = []
   term['$or'].append({'body':{'$regex': ' ' + each}})
   term['$or'].append({'body':{'$regex': each + ' '}})
   query_body['$or'].append(term)

search_query['$or'].append(query_title)
search_query['$or'].append(query_body)

results = questionTable.find(search_query)
for i in results:
   print(i)
'''
'''
use stack
db.createCollection("user")
db.createCollection("question")
db.createCollection("ip")
db.createCollection("answer")

'''

#userTable.remove()
#userTable.insert({'email': "kevin" , 'pass': None} )
#userTable.insert({'email': "nicole" , 'pass': None} )


#print( userTable.find_one({'email':'nicole'})['email']          )

#query = {"email": "mykey"}
#newVal = {"$set": {"key": "KKKK"}}  
#userTable.update_one(query, newVal)
