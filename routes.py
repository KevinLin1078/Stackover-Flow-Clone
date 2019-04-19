from flask import Blueprint, render_template, abort, Flask, request, url_for, json, redirect, Response, session, g
from werkzeug.security import check_password_hash, generate_password_hash
import  datetime
from flask_mail import Mail
from flask_mail import Message
import pymongo 
from pymongo import MongoClient
import time
from bson.objectid import ObjectId
app = Flask(__name__)
client = MongoClient()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] ='ktube110329@gmail.com'
app.config['MAIL_PASSWORD']= '@12345678kn'
mail = Mail(app)
bp = Blueprint('routes', __name__, template_folder='templates')

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

@bp.route('/', methods=['GET'])
def index():
	return redirect(url_for('question.search'))


@bp.route('/adduser', methods=["POST", "GET"])
def adduser():	
	if request.method == "GET":
		print("GET");
		return render_template('adduser.html')
	elif request.method == "POST":
		print("Request Json ======================ADDUSER POST==========================")
		jss = request.json
		print(jss)
		name = jss['username']
		email = jss['email']
		password = jss['password']
		key = 'keykey1212'
		user = 	{ 	
					'username': name, 
					'email': email, 
					'password': password, 
					'verified': 'no',
					'reputation': 1
				}
		userTable.insert(user)
		msg = Message("Hello",sender="ktube110329@gmail.com", recipients=[email])
		msg.body = 'validation key:<' + key +'>'
		mail.send(msg)
		return responseOK({'status':'OK'})



@bp.route('/verify', methods=["POST", "GET"])
def verify():
	if request.method == 'GET':
		return render_template('verify.html')
	elif request.method == 'POST':
		jss =request.json
		print("=========================VERIFY POST===============================")
		print("POST VERIFY JSON" , jss)

		if(jss['key'] == 'abracadabra' or jss['key'] == 'keykey1212'):
			query = {'email' : jss['email']}
			newVal = {"$set": {"verified": "yes" }}  
			userTable.update_one(query, newVal)
		else:
			return responseOK({'status': 'error'})
		return responseOK({'status': 'OK'})

@bp.route('/login', methods=["POST", "GET"])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		jss =request.json
		print("=========================LOGIN POST===============================")
		get_user = userTable.find_one( { 'username': str(jss['username']) } )
		print("Get user ",get_user)
		if( get_user == None):
			return responseOK({'status': 'error'})
			
		if get_user['password'] == jss['password'] and get_user['verified'] == 'yes':
			session.clear()
			session['user'] = jss['username']
			return responseOK({'status': 'OK'})
		else:
			return responseOK({'status': 'error'})
	


@bp.route('/logout', methods=["POST", "GET"])
def logout():
	if request.method =="POST":
		print("=========================LOGOUT POST===============================")
		session.clear()
		return responseOK({'status': 'OK'})


@bp.route('/user/<getName>', methods=["GET"])
def getUser(getName):
	if request.method == 'GET':
		print('=========================/user/<getName>===================================')
		print("name ", getName)
		username = str(getName)
		result = userTable.find_one({'username':username})
		if result == None:
			return responseOK({'status': 'error'})
		user ={	
					'email': result['email'],
					'reputation': result['reputation']
				}
		return responseOK({ 'status': 'OK', 'user': user}) 


@bp.route('/user/<getName>/questions', methods=["GET"])
def getUserQuestions(getName):
	if request.method == 'GET':
		print("=========================USER/<GETNAME> QUESTION==============GET=================")
		username = str(getName)
		print(username)
		result = userTable.find_one({'username':username})
		if result == None:
			return responseOK({'status': 'error'})
		
		allQuestions = questionTable.find({ 'username': username } )
		
		questionReturn = {'status':'OK', 'questions': [] }

		for result in allQuestions:
			questionReturn['questions'].append(str(result['_id']))
		
		return responseOK(questionReturn)

@bp.route('/user/<getName>/answers', methods=["GET"])
def getUserAnnswer(getName):
	if request.method == 'GET':
		print("=========================USER/<GETNAME> QUESTION==============GET=================")
		username = str(getName)
		print(username)
		result = userTable.find_one({'username':username})
		if result == None:
			return responseOK({'status': 'error'})
		allAnswers = answerTable.find({ 'username': username } )
		answerReturn = {'status':'OK', 'answers': [] }

		for result in allAnswers:
			answerReturn['answers'].append(str(result['aid']))
		return responseOK(answerReturn)


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
		
		secret.insert({'ip': request.remote_addr, 'question': title})
		
		username = session['user']
		question =	{
									'user': {	'username': str(username),
														'reputation': 1
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

@app.template_filter('ctime')
def timectime(s):
	return str(time.ctime(s))[3:19] # datetime.datetime.fromtimestamp(s)


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


