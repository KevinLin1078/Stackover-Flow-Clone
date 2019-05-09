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
   questionTable.create_index([('title', pymongo.TEXT),('body', pymongo.TEXT )], name='search_index', default_language='none')

   # filter_with_query("", 1557358154.389, 25, 'timestamp', [], False, True)

def filter_with_query(query, timestamp, limit, sort_by, tags, has_media, accepted):
   client = MongoClient('130.245.170.76', 27017)
   db = client['stack']
   questionTable = db['question']
   time = {"$lte": timestamp}
   tag = {"$all": tags}

   media = {'$not': {'$size': 0}}
   if has_media == False:#if media == flase, then return greater than 0
      media = {'$size': 0}

   accept =  {'$not': {'$eq': None}}
   if accepted == False:
      accept = {'$eq': None}

   allQuestion = None;
   if len(query)== 0:
      print("NO query")
      if len(tags) == 0:
         allQuestion = 	questionTable.find({'timestamp':time, 'media':media , 'accepted_answer_id': accept}).sort([(sort_by, -1)]).limit(limit)
      else:
         allQuestion = 	questionTable.find({'timestamp':time,'tags':tag, 'media':media , 'accepted_answer_id': accept}).sort([(sort_by, -1)]).limit(limit)
   else:
      if len(tags) == 0:
         allQuestion = 	questionTable.find({"$text": {"$search": query }, 'timestamp':time, 'tags': tag, 'media':media , 'accepted_answer_id': accept}).sort([(sort_by, -1)]).limit(limit)
      else:
         allQuestion = 	questionTable.find({"$text": {"$search": query }, 'timestamp':time, 'media':media , 'accepted_answer_id': accept}).sort([(sort_by, -1)]).limit(limit)
   questFilter =[]
   for q in allQuestion:
      temp = {
						'id': str(q['_id']),
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
      questFilter.append(temp)
   return questFilter
# clearMe()
# ppp()

# def connectM():
#    client = MongoClient('130.245.170.76', 27017)
#    db = client['stack']  


# query = "SELECT count(*) FROM imgs WHERE fileID = '" + 'DR5SW9DWY8GUXCEI4EKNW130YGCK3XAQF9JOA41X' + "';"
# row = cassSession.execute(query)[0].count

# print(row)
