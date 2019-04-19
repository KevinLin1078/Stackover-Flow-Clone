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
aidTable = db['answer_id']
questionTable = db['question']
pidTable = db['pid']
ipTable = db['ip']
questionIndex = db['questionIndex']
answerIndex = db['answerIndex']
secret = db['secret']
upvoteTable = db['upvote']




@bp.route('/questions/add', methods=["POST", "GET"])
def addQuestion():
	if request.method == "GET":
		return render_template('addQuestion.html')
	if(request.method == 'POST'):
		print("=========================QUESTION/ADD POST==============nnnnn=================")
		if len(session) == 0:
			print('Wrong SESSION')	
			print("WRONG: ", request.json)
			return responseOK({'status': 'ERROR', 'error': 'Wrong user session'})
		print("JSON ALMOST: ", request.json)
		
		title = None
		body = None
		tags = None
		
		d = request.json
		if ('title' in d) and ('body' in d) and ('tags' in d) :
			title = request.json['title'].encode("utf-8")
			body = request.json['body'].encode("utf-8")
			tags = request.json['tags']
		else:
			return responseOK({'status': 'ERROR', 'error': 'Json key doesnt exist'})
				
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
									'media': None,
									'tags': tags,
									'accepted_answer_id': None,
									'username': str(username),
									'realIP': request.remote_addr
								}
		pid = questionTable.insert(question)
		pid = str(pid)
		
		return responseOK({ 'status': 'OK', 'id':pid}) 

@bp.route('/questions/<IDD>', methods=[ "GET", 'DELETE'])
def getQuestion(IDD):
	pid = ObjectId(str(IDD))
	if request.method == 'GET':
		print("=========================QUESTION/ID====GET===============================")
		print("ID IS: ", pid)

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
				print('USER NOT LOGGED IN AND IP DOES NOT EXIST IN IPDB', ip)
				plus = 1
			else:
				print('USER NOT LOGGED IN AND IP EXISTS IN DB ', ip)

		if len(session) != 0:
			if ipTable.find_one({'ipN': session['user'] , 'pid':pid} ) == None:
				ipTable.insert({'ipN': session['user'], 'pid': pid})
				print('USER IS LOGGED IN AND USER DOES NOT EXIST IN IPDB', ip)
				plus = 1
			else:
				print('USER IS LOGGED IN AND USER EXISTS IN IPDB', ip)
		
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
		user = result['user']
		question = 	{ 	'status':'OK',
							"question": {
									"score": score,
									"view_count": view_count,
									"answer_count": 0,
									"media": None,
									"tags": tags,
									"accepted_answer_id": None,
									"title": title,
									"body": body,
									"id": pid,
									"timestamp": timestamp,
									"user": user
									},
							 "answers":[]
						}
		'''THIS PART IS FOR HTML'''		
		allAnswers = answerTable.find({'pid': ObjectId(pid)})
		for result in allAnswers:
			temp =	{
						'user': result['user'],
						'answer': result['body']
					}
			question['answers'].append(temp)
		'''This Part Needs to be deleted'''
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
			return responseOK({'status': 'error','error': 'not logged in'})
		pid = ObjectId(str(IDD))
		body = request.json['body']
		media = None
		print('================--===========/questions/<IDD>/answers/add===============--====================')
		print("ANSWER JSON: ", request.json)

		if ('media' in request.json):
			media = request.json['media']

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
		return responseOK({'status': 'OK', 'id': str(aid)})

@bp.route('/questions/<IDD>/answers', methods=['GET'])
def getAnswers(IDD):
	if request.method == 'GET':
		print('================--===========/questions/<IDD>/answers===============--====================')
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
						'media': None
					}

			answerReturn['answers'].append(temp)
		print(answerReturn)

		return responseOK(answerReturn)

@bp.route('/questions/<IDD>/upvote', methods=['POST'])
def upvoteQuestion(IDD):
	if request.method == 'POST':
		pid = str(IDD)
		print('===========================/questions/<IDD>/upvote===================================')
		if len(session) == 0:
			return responseOK({'status': 'error','error': 'Please login to upvote question'})
		upvote = request.json['upvote']
		user = session['user']
		result = upvoteTable.find_one({'username' : user, 'pid': pid} )
		
		if upvote == True:
			if result == None:
				upvoteTable.insert({'username': user, 'pid': pid, 'vote': 1})
				updateScore(pid, user, 1)
			elif result['vote'] ==  1:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': 0} } )
				update_score(pid, user, -1)	
			elif result['vote'] ==  0:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': 1} } )
				update_score(pid, user, 1)
			elif result['vote'] == -1:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': 1} } )
				update_score(pid, user, 2)
		#################################################FALSE##########################################
		elif upvote == False:
			if result == None:
				upvoteTable.insert({'username': user, 'pid': pid, 'vote': -1})
				updateScore(pid, user, -1)
			elif result['vote'] ==  -1:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': 0} } )
				update_score(pid, user, 1)	
			elif result['vote'] ==  0:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': -1} } )
				update_score(pid, user, -1)
			elif result['vote'] == 1:
				upvoteTable.update_one({'username':user, 'pid': pid} , { "$set": {'vote': -1} } )
				update_score(pid, user, -2)
		return responseOK({'status': 'OK'})

@bp.route('/questions/<IDD>/upvote', methods=['POST'])
def upvoteAnswer():
	if request.method == 'POST':
		pid = str(IDD)
		print('===========================/questions/<IDD>/upvote===================================')
		if len(session) == 0:
			return responseOK({'status': 'error','error': 'Please login to upvote answer'})
		upvote = request.json['upvote']



@bp.route('/searchOK', methods=['GET'])
def searchOK():
	if request.method == 'GET':
		result = questionTable.find()
		login= 0
		if len(session) == 0:
			login = 0
		else:
			login = 1
		return render_template('questionTable.html', questionTable=result, login= login)

@bp.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		result = questionTable.find()
		login= 0
		if len(session) == 0:
			login = 0
		else:
			login = 1
		return render_template('questionTable.html', questionTable=result, login= login)
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

def update_score(pid, user, val):
	question = questionTable.find_one( {'_id': ObjectId(pid)} )
	new_score = question['score'] + val							#plus one to question
	questionTable.update_one( {'_id': ObjectId(pid)} , { "$set": {'score': new_score} } )
	
	user_filter = userTable.find_one({'username': user})	#plus one to user reputation
	new_rep = user_filter['reputation']
	if new_rep == 1 and val < 0:
		pass
	else:
		userTable.update_one({'username': user}, { "$set": {'reputation': new_rep + val} } )

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