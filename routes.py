from flask import Blueprint, render_template, abort, Flask, request, url_for, json, redirect, Response, session, g
from werkzeug.security import check_password_hash, generate_password_hash
import  datetime
from flask_cors import CORS
from flask_mail import Mail
from flask_mail import Message
import pymongo 
from pymongo import MongoClient
import time
app = Flask(__name__)
client = MongoClient()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] ='ktube110329@gmail.com'
app.config['MAIL_PASSWORD']= '@12345678kn'
#app.config.update(dict(DEBUG=True, MAIL_SERVER = 'smtp.gmail.com',MAIL_PORT = 587,MAIL_USE_TLS = True,MAIL_USE_SSL = False,MAIL_USERNAME = 'bluekevin61@gmail.com',MAIL_PASSWORD = 'QWERTYUIO'))
mail = Mail(app)
bp = Blueprint('routes', __name__, template_folder='templates')
CORS(bp)

db = client.stack
userTable = db['user'] 
answerTable = db['answer']
aidTable = db['answer_id']
questionTable = db['question']
pidTable = db['pid']
ipTable = db['ip']
questionIndex = db['questionIndex']
answerIndex = db['answerIndex']

@bp.route('/', methods=['GET'])
def index():
	return redirect(url_for('routes.search'))


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
		
		user = 	{ 	'username': name, 
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
		print("POST LOGIN JSON" , jss)
		get_user = userTable.find_one( { 'username': str(jss['username']) } )
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
		username = str(getName)
		result = userTable.find_one({'username':username})

		user ={	'email': result['email'],
					'reputation': result['reputation']
				}
		return responseOK({ 'status': 'OK', 'user': user}) 


@bp.route('/user/<getName>/questions', methods=["GET"])
def getUserQuestions(getName):
	if request.method == 'GET':
		print("=========================USER/<GETNAME> QUESTION==============GET=================")
		username = str(getName)
		query = 	{ 'user': {'username': username} }
		allQuestions = question.find(query)

		questionReturn = {'status':'OK', 'questions': [] }

		for result in allQuestions:
			temp = str(result['pid'])
			questionReturn['questions'].append(temp)
		
		return responseOK(questionReturn)

# @bp.route('/user/<getName>/answers', methods=["GET"])
# def getUserAnswers(getName):
# 	if request.method == 'GET':
# 		pass


@bp.route('/questions/add', methods=["POST", "GET"])
def addQuestion():
	if(request.method == 'POST'):
		print("=========================QUESTION/ADD POST==============nnnnn=================")
		if len(session) == 0:
			print('Wrong SESSION')	
			print("WRONG: ", request.json)
			return responseOK({'status': 'ERROR', 'error': 'Wrong user session'})
		print("JSON ALMOST: ", request.json)
		
		
		pid = pidTable.find_one({'pid':'pid'})['id']
		pidTable.update_one({'pid':'pid'}, {"$set": {"id": pid+1 }} )
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
		question =	{
									'pid' : pid,         # id of question
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
									'accepted_answer_id': None
								}
		pid = str(pid)
		questionStore(title, body, pid)
		questionTable.insert(question, check_keys=False)
		return responseOK({ 'status': 'OK', 'id':pid}) 

@bp.route('/questions/<IDD>', methods=[ "GET", 'DELETE'])
def getQuestion(IDD):
	pid = int(IDD)
	if request.method == 'GET':
		print("=========================QUESTION/ID====GET===============================")
		print("ID IS: ", pid)
		result = questionTable.find_one({'pid':pid})
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
		
		print('VALUE ADDED TO VIEW COUNT: ', plus)
		
		count = result['view_count']
		questionTable.update_one({'pid':pid}, { "$set": {'view_count': count + plus}} )
		result = questionTable.find_one({'pid':pid})

		score = result['score']
		view_count = result['view_count']
		answer_count = result['answer_count']
		media = result['media']
		tags = result['tags']
		title = result['title']
		body = result['body']
		pid = str(result['pid'])
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
										}
						}
		return responseOK(question)
	elif request.method == 'DELETE':
		print("=========================QUESTION/ID====DELETE===============================")
		if len(session) == 0:
			print("CANT DELETE USER NOT LOGGED IN")
			return responseOK({'status':'error'})
		else:
			result = questionTable.find_one({'pid':pid})
			if( result == None):
				print('FAILED DELTED, invalid QUESTIONS ID')
				return responseNO({'status':'error'})

			username = result['user']['username']
			if session['user'] != username:
				print('FAILED DELTED, user is not original')
				return responseNO({'status':'error'})
			else:
				print('SUCCESSFULLY DELTED, user is original')
				pid = int(pid)
				questionTable.delete_one({'pid': pid})
				answerTable.delete_one({'pid': pid})
				ipTable.delete_many({'pid': pid})
				return responseOK({'status': 'OK'})
				

@bp.route('/questions/<IDD>/answers/add', methods=["POST", "GET"])
def addAnswer(IDD):
	if request.method == 'POST':
		if len(session) == 0:
			return responseOK({'status': 'error','error': 'not logged in'})
		pid = int(IDD)
		body = request.json['body']
		media = None
		print('================--===========/questions/<IDD>/answers/add===============--====================')
		print("ANSWER JSON: ", request.json)

		if ('media' in request.json):
			media = request.json['media']

		userID = userTable.find_one({'username': session['user']})['_id']
		userID = str(userID)

		aid = aidTable.find_one({'aid':'aid'})['id']
		aidTable.update_one({'aid': 'aid'}, {"$set": {"id": aid+1 }} )
		answer = 	{
					'pid': pid,
					'body':body,
					'media': media,
					'aid': aid,
					'user': session['user'],
					'userID':  userID,
					'timestamp': (time.time()),
					'is_accepted': False,
					'score' : 0
					}
		answerTable.insert(answer)
		return responseOK({'status': 'OK', 'id': str(aid)})

@bp.route('/questions/<IDD>/answers', methods=['GET'])
def getAnswers(IDD):
	if request.method == 'GET':
		print('================--===========/questions/<IDD>/answers===============--====================')
		pid = int(IDD)
		allAnswers = answerTable.find({'pid': pid})
		answerReturn = {"status":"OK", 'answers': []}

		for result in allAnswers:
			temp =	{
						'id': str(result['aid']),
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
		
@bp.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		return render_template('questionTable.html', questionTable=questionTable.find())
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
			query = request.json['q'].encode("utf-8").strip()
		print("query: ", query)
		print("timestamp: ", timestamp )
		print("limit: ", limit)
		
		if len(query) == 0:
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
							'id': str(q['pid']),
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
				
			return responseOK({'status':'OK','questions': ret,'error':"" })
		else:
			print("WITH QUERY")
			questFilter = []
			allQuestion = questionTable.find();
			for q in allQuestion:
				if q['timestamp'] <= timestamp:
					questFilter.append(q)
			print('THERE ARE ', len(questFilter))
			questFilter.sort(key=lambda x: x['timestamp'], reverse=True)

			ret = []  
			count = 0;
			ranking = rank(query.lower())

			for item in ranking:
				for q in questFilter:
					if(count == limit ):
						break;
					if str(item[0]) == str(q['pid']):
						temp = {
								'id': str(q['pid']),
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

			ret.sort(key=lambda x: x['timestamp'], reverse=True)
			return responseOK({'status':'OK','questions': ret,'error':"" })


def responseOK(stat):
	data = stat
	jsonData = json.dumps(data)
	respond = Response(jsonData,status=200, mimetype='application/json')
	return respond

def responseNO(stat):
	data = stat
	jsonData = json.dumps(data)
	respond = Response(jsonData,status=204, mimetype='application/json')
	return respond

def questionStore(title, body, pid):
   parseAlgo(title, pid)
   parseAlgo(body, pid)

def parseAlgo(body, pid):
   body = str(body).split()
   if len(body) != 0:
      for word in body:
         result = questionIndex.find_one({word: word})
         if result == None:
            questionIndex.insert({ word: word, 'arr': [[pid,1]]  }, check_keys=False)
         else:
            arr = result['arr']
            found = False
            for i in range(0, len(arr)):
               if arr[i][0] == pid:
                  arr[i][1]+=1
                  found = True
                  break
            if found == True:      
               questionIndex.update_one({word:word}, {'$set': {'arr': arr  }}  )
            else:
               questionIndex.update_one({word:word}, {'$push': {'arr': [pid, 1]  }}  )



def rank(body):
	b = body
	body = str(body).split()
	diction = {}
	print("ranking body .... ", body)
	for word in body:
		word = word.encode("utf-8")
		print("word is : ", word)
		arr = questionIndex.find_one({word:word})
		if arr != None:
			arr = arr['arr']
			for item in arr:
				key = str(item[0]).encode("utf-8")
				if key not in diction:
					diction[key] = 1
				else:
					diction[key] +=1
	import operator
	sorted_d = sorted(diction.items(), key=operator.itemgetter(1), reverse=True)  
	return sorted_d
'''
def rank(body):
   b = body
   body = str(body).split()
   diction = {}

   for word in body:
      arr = questionIndex.find_one({word:word})
		arr =arr['arr']
		print("ranking .... ", arr)
      for item in arr:
         key = str(item[0])
         if key not in diction:
            diction[key] = 1
         else:
            diction[key] +=1
   print(diction)
   import operator
   sorted_d = sorted(diction.items(), key=operator.itemgetter(1), reverse=True)  
   print(sorted_d)
   return sorted_d
'''