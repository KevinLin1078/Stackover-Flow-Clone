from flask import Flask 
import pymongo 
from pymongo import MongoClient
from bson.objectid import ObjectId

def clearMe():
   client = MongoClient()
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


# client = MongoClient()
# db = client['stack']  
# questionTable = db['question']

def filter_without_query(timestamp, limit, sort_by, tags, has_media, accepted):
   print("NO QUERY" ,(timestamp, limit, sort_by, tags, has_media, accepted))

   questFilter = []
   allQuestion = questionTable.find();
   for q in allQuestion:
      if q['timestamp'] <= timestamp:
         questFilter.append(q)
   print('THERE ARE ', len(questFilter))
   questFilter.sort(key=lambda x: x[sort_by], reverse=True)

   accept_arr = []  
   if accepted == False:
      acceptFalse(questFilter, accept_arr)
   if accepted == True:
      acceptTrue(questFilter, accept_arr)
   
   mediaArr = []
   if has_media == True:
      mediaTrue(accept_arr, mediaArr)
   if has_media == False:
      mediaFalse(accept_arr, mediaArr)


   return mediaArr[0:limit]



def mediaTrue(questFilter, ret):
	for q in questFilter:
		if len(q['media']) != 0:
			temp = {
						'id': q['id'],
						'title':q['title'],
						'body': q['body'],
						'tags': q['tags'],
						'answer_count': 0,
						'media': q['media'],
						'accepted_answer_id': q['accepted_answer_id'] ,
						'user':q['user'],
						'timestamp': q['timestamp'],
						'score': q['score'],
						"view_count": q['view_count']
					}
			ret.append(temp)

def mediaFalse(questFilter, ret):
	for q in questFilter:
		if q['media'] == []:
			temp = {
						'id': q['id'],
						'title':q['title'],
						'body': q['body'],
						'tags': q['tags'],
						'answer_count': 0,
						'media': q['media'],
						'accepted_answer_id': q['accepted_answer_id'] ,
						'user':q['user'],
						'timestamp': q['timestamp'],
						'score': q['score'],
						"view_count": q['view_count']
					}
			ret.append(temp)

def acceptFalse(questFilter, ret):
   for q in questFilter:
         if q['accepted_answer_id'] == None:
            temp = {
               'id': q['_id'],
               'title':q['title'],
               'body': q['body'],
               'tags': q['tags'],
               'answer_count': 0,
               'media': q['media'],
               'accepted_answer_id': q['accepted_answer_id'] ,
               'user':q['user'],
               'timestamp': q['timestamp'],
               'score': q['score'],
               "view_count": q['view_count']
            }
            ret.append(temp)
def acceptTrue(questFilter, ret):
   for q in questFilter:
         if q['accepted_answer_id'] != None:
            temp = {
               'id': q['_id'],
               'title':q['title'],
               'body': q['body'],
               'tags': q['tags'],
               'answer_count': 0,
               'media': q['media'],
               'accepted_answer_id': q['accepted_answer_id'] ,
               'user':q['user'],
               'timestamp': q['timestamp'],
               'score': q['score'],
               "view_count": q['view_count']
            }
            ret.append(temp)




def play():
   arr = filter_without_query(1556171357.110906, 25, 'timestamp', [], True, True)
   for a in arr:
      print(a['title'])
   print(len(arr), 'slim body')

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
