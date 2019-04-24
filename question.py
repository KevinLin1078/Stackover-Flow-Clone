from flask import Blueprint, render_template, abort, Flask, request, url_for, json, redirect, Response, session, g
from werkzeug.security import check_password_hash, generate_password_hash
import  datetime
from flask_mail import Mail
from flask_mail import Message
import pymongo 
from pymongo import MongoClient
import time
from bson.objectid import ObjectId

client = MongoClient()
bp = Blueprint('question', __name__, template_folder='templates')

db = client.stack
userTable = db['user'] 
answerTable = db['answer']
questionTable = db['question']
ipTable = db['ip']
upvoteTable = db['upvote']
mediaTable = db['mediaID']


from cassandra.cluster import Cluster
cluster = Cluster()
cassSession = cluster.connect(keyspace='hw5')


@bp.route('/questions/add', methods=["POST", "GET"])
def addQuestion():
	if request.method == "GET":
		return render_template('addQuestion.html')
	if(request.method == 'POST'):
		if len(session) == 0:
			print('Add Question Wrong SESSION')	
			return responseOK({'status': 'error', 'error': 'Wrong user session'})
		title = None
		body = None
		tags = None
		media = []
		d = request.json
		

		if 'media' in d:
			media = request.json['media']
			print('Quesiotns/ADD +++++++++++++++++++++++++++++MEDIA: ', media)
			if len(media) != 0:
				for item in media:
						is_found = mediaTable.find_one({"mediaID": item})
						if is_found:
							print('Media ID FOUND IN ANOTHER QUESTION ')
							return responseOK({ 'status': 'error', 'error':"media ID already exists"}) 
						
						query = "SELECT * FROM imgs WHERE fileID = '" + item + "';"
						row = cassSession.execute(query)[0]
						name = row[3]
						if name != session['user']:
							return responseOK({ 'status': 'error', 'error':"media does not belong to poster"}) 

		if ('title' in d) and ('body' in d) and ('tags' in d) :
			title = request.json['title'].encode("utf-8")
			body = request.json['body'].encode("utf-8")
			tags = request.json['tags']
		else:
			return responseOK({'status': 'error', 'error': 'Json key doesnt exist'})
				
		username = session['user']
		user_filter = userTable.find_one({'username': username})
		reputation = user_filter['reputation']
		question =	{
									'user': {	'username': str(username),
														'reputation': reputation
													},
									'title': title, 
									'body': body,
									'score': 0,
									'view_count': 0,
									'answer_count': 0,
									'timestamp': int(time.time()),
									'media': media,
									'tags': tags,
									'accepted_answer_id': None,
									'username': str(username),
									'realIP': request.remote_addr
								}
		pid = questionTable.insert(question)
		pid = str(pid)
		for item in media:
			mediaTable.insert({"mediaID": item, 'pid': pid})

		return responseOK({ 'status': 'OK', 'id':pid}) 

@bp.route('/questions/<IDD>', methods=[ "GET", 'DELETE'])
def getQuestion(IDD):
	pid = ObjectId(str(IDD))
	if request.method == 'GET':
		#print("=========================QUESTION/ID====GET===============================")
		result = questionTable.find_one({"_id": pid})

		if( result == None):
			print("QUESTION ID DOESNT EXIST")
			print(request.remote_addr)
			return responseOK({'status':'error', 'error': 'id doesnt exist'})
		ip = request.remote_addr
		ip = str(ip)
		plus = 0

		if len(session) == 0:
			if ipTable.find_one({'ip':ip , 'pid':pid}) == None:
				ipTable.insert({'ip':ip, 'pid': pid})
				plus = 1
		if len(session) != 0:
			if ipTable.find_one({'ipN': session['user'] , 'pid':pid} ) == None:
				ipTable.insert({'ipN': session['user'], 'pid': pid})
				plus = 1
		
		count = result['view_count']
		questionTable.update_one({'_id':pid}, { "$set": {'view_count': count + plus}} )
		result = questionTable.find_one({'_id':pid})
		score = result['score']
		view_count = result['view_count']
		answer_count = result['answer_count']
		media = result['media']
		tags = result['tags']
		title = result['title']
		body = result['body']
		pid = str(result['_id'])
		timestamp = result['timestamp']
		
		user = result['user']['username']
		reputation = userTable.find_one({'username':user})
		reputation = reputation['reputation']

		question = 	{ 	'status':'OK',
							"question": {
									"score": score,
									"view_count": view_count,
									"answer_count": 0,
									"media": media,
									"tags": tags,
									"accepted_answer_id": None,
									"title": title,
									"body": body,
									"id": pid,
									"timestamp": timestamp,
									"user": {
												'username': user,
												'reputation' :reputation
											}
									}
						}
		return responseOK(question)

	elif request.method == 'DELETE':
		print("=========================QUESTION/ID====DELETE===============================")
		if len(session) == 0:
			print("CANT DELETE USER NOT LOGGED IN")
			return responseNO({'status':'error', 'error': 'user not logged in'})
		else:
			pid = ObjectId(str(IDD))
			result = questionTable.find_one({'_id':pid})
			if( result == None):
				print('FAILED DELTED, invalid QUESTIONS ID')
				return responseNO({'status':'error','error':'Question does not exist'})

			username = result['user']['username']
			if session['user'] != username:
				print('FAILED DELTED, user is not original')
				return responseNO({'status':'error', 'error': 'Not orginal user'})
			else:
				print('SUCCESSFULLY DELTED, user is original')
				questionTable.delete_one({'_id': pid})
				answerTable.delete_one({'pid': pid})
				ipTable.delete_many({'pid': pid})
				return responseOK({'status': 'OK'})
				

@bp.route('/questions/<IDD>/answers/add', methods=["POST", "GET"])
def addAnswer(IDD):
	if request.method == 'POST':
		if len(session) == 0:
			print("NO session answer")
			return responseOK({'status': 'error','error': 'not logged in'})
		pid = ObjectId(str(IDD))
		body = request.json['body']
		media = []
		
		if ('media' in request.json):
			media = request.json['media']
			print('Answers/ADD media: ++++++++++++++++++++++ANSWER++++++MEDIA ', media)
			if len(media) != 0:
				for item in media:
						is_found = mediaTable.find_one({"mediaID": item})
						if is_found != None: #if id exist already, return error
							return responseOK({ 'status': 'error', 'error':"media ID already exists"}) 
						
						query = "SELECT * FROM imgs WHERE fileID = '" + item + "';"
						row = cassSession.execute(query)[0]
						name = row[3]
						if name != session['user']:
							return responseOK({ 'status': 'error', 'error':"media does not belong to poster"}) 

		userID = userTable.find_one({'username': session['user']})['_id']
		userID = str(userID)
		
		answer = 	{
					'pid': pid,
					'body':body,
					'media': media,
					'user': session['user'],
					'userID':  userID,
					'timestamp': (time.time()),
					'is_accepted': False,
					'score' : 0,
					'username': session['user']
					}
		aid = answerTable.insert(answer)
		aid = str(aid)

		if len(media) != 0:
			for item in media:
					is_found = mediaTable.find_one({"mediaID": item})
					if is_found == None:
						mediaTable.insert({"mediaID": item, 'aid': aid})
					else:
						return responseOK({ 'status': 'error', 'error':"media ID already exists"}) 

		return responseOK({'status': 'OK', 'id': str(aid)})

@bp.route('/questions/<IDD>/answers', methods=['GET'])
def getAnswers(IDD):
	if request.method == 'GET':
		
		pid = ObjectId(str(IDD))
		allAnswers = answerTable.find({'pid': pid})
		answerReturn = {"status":"OK", 'answers': []}

		for result in allAnswers:
			temp =	{
						'id': str(result['_id']),
						'user': result['user'],
						'body': result['body'],
						'score': result['score'],
						'is_accepted': result['is_accepted'],
						'timestamp': result['timestamp'],
						'media': result['media']
					}
			answerReturn['answers'].append(temp)
		print(answerReturn)

		return responseOK(answerReturn)

@bp.route('/questions/<IDD>/upvote', methods=['POST'])
def upvoteQuestion(IDD):
	if request.method == 'POST':
		pid = str(IDD)
		if len(session) == 0:
			print('upvote Wrong session')
			return responseOK({'status': 'error','error': 'Please login to upvote question'})
		print('===========================/questions/<IDD>/upvote===================================')
		upvote = request.json['upvote']
		user = session['user']
		print ([pid, upvote, user]  )
		result = upvoteTable.find_one({'username' : user, 'pid': pid} )
		questionResult = questionTable.find_one( {'_id': ObjectId(str(IDD)) })
		realUser = questionResult['username']
		if upvote == True:
			if result == None:
				upvoteTable.insert({'username': user, 'pid': pid, 'vote': 1})
				updateQuestionScore(pid, realUser, 1, 1)
			elif result['vote'] ==  1:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': 0} } )
				updateQuestionScore(pid, realUser, -1,-1)	
			elif result['vote'] ==  0:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': 1} } )
				updateQuestionScore(pid, realUser, 1, 1)
			elif result['vote'] == -1:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': 1} } )
				updateQuestionScore(pid, realUser, 2, 1)
		#################################################FALSE##########################################
		elif upvote == False:
			if result == None:
				upvoteTable.insert({'username': user, 'pid': pid, 'vote': -1})
				updateQuestionScore(pid, realUser, -1, -1)
			elif result['vote'] ==  -1:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': 0} } )			
				updateQuestionScore(pid, realUser, 1, 1)	
			elif result['vote'] ==  0:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': -1} } )
				updateQuestionScore(pid, realUser, -1, -1)
			elif result['vote'] == 1:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': -1} } )
				updateQuestionScore(pid, realUser, -2, -1)
		return responseOK({'status': 'OK'})

@bp.route('/answers/<IDD>/upvote', methods=['POST'])
def upvoteAnswer(IDD):
	if request.method == 'POST':
		aid = str(IDD)
		
		if len(session) == 0:
			return responseOK({'status': 'error','error': 'Please login to upvote answer'})
		print('===========================/answers/<IDD>/upvote===================================')
		upvote = request.json['upvote']
		user = session['user']
		print ([aid, upvote, user]  )
		result = upvoteTable.find_one({'username' : user, 'aid': aid} )
		answerResult = answerTable.find_one( {'_id': ObjectId(str(IDD)) })
		realUser = answerResult['username']
		if upvote == True:
			if result == None:
				upvoteTable.insert({'username': user, 'aid': aid, 'vote': 1})
				updateAnswerScore(aid, realUser, 1,1)	
			elif result['vote'] ==  1:
				upvoteTable.update_one({'username':user, 'aid': aid} , { "$set": {'vote': 0} } )
				updateAnswerScore(aid, realUser, -1,-1)	
			elif result['vote'] ==  0:
				upvoteTable.update_one({'username':user, 'aid': aid} , { "$set": {'vote': 1} } )
				updateAnswerScore(aid, realUser, 1, 1)
			elif result['vote'] == -1:
				upvoteTable.update_one({'username':user, 'aid': aid} , { "$set": {'vote': 1} } )
				updateAnswerScore(aid, realUser, 2, 1)
		#################################################FALSE##########################################
		elif upvote == False:
			if result == None:
				upvoteTable.insert({'username': user, 'aid': aid, 'vote': -1})
				updateAnswerScore(aid, realUser, -1, -1)
			elif result['vote'] ==  -1:
				upvoteTable.update_one({'username':user, 'aid': aid} , { "$set": {'vote': 0} } )			
				updateAnswerScore(aid, realUser, 1, 1)	
			elif result['vote'] ==  0:
				upvoteTable.update_one({'username':user, 'aid': aid} , { "$set": {'vote': -1} } )
				updateAnswerScore(aid, realUser, -1, -1)
			elif result['vote'] == 1:
				upvoteTable.update_one({'username':user, 'aid': aid} , { "$set": {'vote': -1} } )
				updateAnswerScore(aid, realUser, -2, -1)
		return responseOK({'status': 'OK'})



# @bp.route('/answers/<IDD>/accept', methods=['POST'])
# def acceptAnswer(IDD):


@bp.route('/searchME', methods=['GET'])
def searchOK():
	if request.method == 'GET':
		result = questionTable.find()
		login= 0
		if len(session) == 0:
			login = 0
		else:
			login = 1
		return render_template('questionTable.html', questionTable=result, login= login)

@bp.route('/search', methods=['POST'])
def search():
	if request.method == 'POST':
		print('--------------------------------Search-----------------------------')
		timestamp = time.time()
		if 'timestamp' not in request.json:
			print("timestamp doesntt exist")
			timestamp = time.time()
		else:
			timestamp = request.json['timestamp']
		
		limit = 25
		if 'limit' not in request.json:
			print("Limit doesntt exist")
			limit = 25
		else:
			limit = int( request.json['limit'])			
		
		if 'limit' in request.json:
			limit = request.json['limit']
		
		query = ''
		if 'q' in request.json:
			query = request.json['q'].encode("utf-8").strip().lower()
		print("query: ", query)
		print("timestamp: ", timestamp )
		print("limit: ", limit)
		
		if len(query) == 0:
			answer = filter_without_query(timestamp, limit)
			return responseOK(answer)
		else:
			answer = filter_with_query(query, timestamp, limit)
			return responseOK(answer)


def responseOK(stat):
	data = stat
	jsonData = json.dumps(data)
	respond = Response(jsonData,status=200, mimetype='application/json')
	return respond

def responseNO(stat):
	data = stat
	jsonData = json.dumps(data)
	respond = Response(jsonData,status=404, mimetype='application/json')
	return respond


def updateQuestionScore(pid, user, qval, uval):
	question = questionTable.find_one( {'_id': ObjectId(pid)} )
	new_score = question['score'] + qval							#plus one to question
	questionTable.update_one( {'_id': ObjectId(pid)} , { "$set": {'score': new_score} } )
	
	user_filter = userTable.find_one({'username': user})	#plus one to user reputation
	new_rep = user_filter['reputation']
	if new_rep == 1 and uval < 0:
		print('CANNOT ADD TO USER REP ', uval)
		return
	new_repp = new_rep + uval
	print("NEW REPP +++++++++++++++++ " ,new_repp )
	userTable.update_one({'username': user}, { "$set": {'reputation': new_repp} } )


def updateAnswerScore(aid, user, aval, uval):
	answer = answerTable.find_one( {'_id': ObjectId(aid)} )
	new_score = answer['score'] + aval							#plus one to answer
	answerTable.update_one( {'_id': ObjectId(aid)} , { "$set": {'score': new_score} } )
	
	user_filter = userTable.find_one({'username': user})	#plus one to user reputation
	new_rep = user_filter['reputation']
	if new_rep == 1 and uval < 0:
		print('CANNOT ADD TO USER REP ', uval)
		return
	new_repp = new_rep + uval
	userTable.update_one({'username': user}, { "$set": {'reputation': new_repp} } )

def filter_with_query(query, timestamp, limit):
	print("WITH QUERY")
	search_query = {}
	search_query['$or'] = []

	query_title = {}
	query_title['$or'] = []

	query_body = {}
	query_body['$or'] =[]
	query = query.lower()
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

	ret =[]
	count = 0
	for q in results:
		if(count == limit ):
			break;
		if q['timestamp'] <= timestamp:
			temp = {
							'id': str(q['_id']),
							'title':q['title'],
							'body': q['body'],
							'tags': q['tags'],
							'answer_count': 0,
							'media': None,
							'accepted_answer_id': None,
							'user':q['user'],
							'timestamp': q['timestamp'],
							'score': 0,
							"view_count": q['view_count']
						}
			count = count + 1
			ret.append(temp)			
	ret.sort(key=lambda x: x['timestamp'], reverse=True)
	return {'status':'OK','questions': ret,'error':"" }

def filter_without_query(timestamp, limit):
	print("NO QUERY")
	questFilter = []
	allQuestion = questionTable.find();
	for q in allQuestion:
		if q['timestamp'] <= timestamp:
			questFilter.append(q)
	print('THERE ARE ', len(questFilter))
	questFilter.sort(key=lambda x: x['timestamp'], reverse=True)

	ret = []  
	count = 0;
	for q in questFilter:
		if(count == limit ):
			break;
		temp = {
					'id': str(q['_id']),
					'title':q['title'],
					'body': q['body'],
					'tags': q['tags'],
					'answer_count': 0,
					'media': None,
					'accepted_answer_id': None,
					'user':q['user'],
					'timestamp': q['timestamp'],
					'score': 0,
					"view_count": q['view_count']
				}
		count = count +1
		ret.append(temp)
		
	return {'status':'OK','questions': ret,'error':"" }