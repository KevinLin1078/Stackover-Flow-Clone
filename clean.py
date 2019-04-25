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


client = MongoClient()
db = client['stack']  
questionTable = db['question']

def filter_without_query(timestamp, limit, sort_by, tags, has_media, accepted):
	print("NO QUERY")
	questFilter = []
	allQuestion = questionTable.find();
	for q in allQuestion:
		if q['timestamp'] <= timestamp:
			questFilter.append(q)
	print('THERE ARE ', len(questFilter))
	questFilter.sort(key=lambda x: x[sort_by], reverse=True)

	accept_arr = []  
	if accepted == True:
		acceptTrue(questFilter, accept_arr)
	elif accepted == False:
		acceptFalse(questFilter, accept_arr)
	
	mediaArr = []
	if has_media == True:
		mediaTrue(accept_arr, mediaArr)
	elif has_media == False:
		mediaFalse(accept_arr, mediaArr)
	
	tagArr = []
	if len(tags) == 0:
		return {'status':'OK','questions': mediaArr[0:limit],'error':"Without Query Media " +str(len(mediaArr[0:limit])) }
	else:
		tagFinder(mediaArr, tagArr, tags)

	return {'status':'OK','questions': tagArr[0:limit],'error':"Without Query" + str(len(tagArr[0:limit]))  }


def acceptTrue(questFilter, ret):
	for q in questFilter:
		if q['accepted_answer_id'] != None:
			temp = {
						'id': str(q['_id']),
						'title':q['title'],
						'body': q['body'],
						'tags': q['tags'],
						'answer_count': 0,
						'media': q['media'],
						'accepted_answer_id': q['accepted_answer_id'],
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
			ret.append(temp)

def mediaTrue(questFilter, ret):
	for q in questFilter:
		if q['media'] != []:
			temp = {
						'id': str(q['id']),
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
						'id': str(q['id']),
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
   arr = filter_without_query(1556178209.562155, 25, 'timestamp', ['html', 'css'], False, False)
   arr = arr['questions']
   for a in arr:
      print(a['title'])
   print(len(arr), 'slim body')




# from cassandra.cluster import Cluster
# cluster = Cluster()
# cassSession = cluster.connect(keyspace='hw5')


# query = "SELECT count(*) FROM imgs WHERE fileID = '" + 'DR5SW9DWY8GUXCEI4EKNW130YGCK3XAQF9JOA41X' + "';"
# row = cassSession.execute(query)[0].count

# print(row)