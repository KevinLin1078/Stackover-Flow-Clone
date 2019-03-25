from flask import Blueprint, render_template, abort, Flask, request, url_for, json, redirect, Response, session, g
from werkzeug.security import check_password_hash, generate_password_hash
import tictac, datetime
from flask_cors import CORS
from flask_mail import Mail
from flask_mail import Message
import pymongo 
from pymongo import MongoClient

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

@bp.route('/', methods=['GET','POST'])
def index():
	return redirect(url_for('routes.login'))


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
					'verified': 'no'
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
# db = client.stack
# userTable = db['user'] 
# answerTable = db['answer']
# aidTable = db['answer_id']
# questionTable = db['question']
# pidTable = db['pid']
import time

@bp.route('/questions/add', methods=["POST", "GET"])
def addQuestion():
	if(request.method == 'POST'):
		print("=========================QUESTION/ADD POST==============nnnnn=================")
		if len(session) == 0:
			print('Wrong SESSION')	
			print("WRONG: ", request.json)
			return responseOK({'status': 'ERROR', 'error': 'Wrong user session'})
		print("JSON ALMOST: ", request.json)
		print("HERE1")
		
		pid = pidTable.find_one({'pid':'pid'})['id']
		pidTable.update_one({'pid':'pid'}, {"$set": {"id": pid+1 }} )
		title = None
		body = None
		tags = None
		
		d = request.json

		if ('title' in d) and ('body' in d) and ('tags' in d) :
			title = request.json['title']
			body = request.json['body']
			tags = request.json['tags']
		else:
			return responseOK({'status': 'ERROR', 'error': 'Json key doesnt exist'})

		username = session['user']
		print("HERE2")
		print("USER ", username)
		question =	{	'username': username, 
						'title': title, 
						'tags': tags, 
						'view_count': 0,
						'time' : (time.time()),
						'pid' : pid,         # id of question
						'media': None,
						'body': body
					}
		
		pid = str(pid)
		questionTable.insert(question)

		return responseOK({ 'status': 'OK', 'id':pid}) 

@bp.route('/questions/<IDD>', methods=["POST", "GET"])
def getQuestion(IDD):
	if request.method == 'GET':
		print("=========================QUESTION/ID====ID===ID========================")
		pid = int(IDD)
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
				plus = 0

		if len(session) != 0:
			if ipTable.find_one({'ipN': session['user'] , 'pid':pid} ) == None:
				ipTable.insert({'ipN': session['user'], 'pid': pid})
				print('USER IS LOGGED IN AND USER DOES NOT EXIST IN IPDB', ip)
				plus = 1
			else:
				print('USER IS LOGGED IN AND USER EXISTS IN IPDB', ip)
				plus = 0
		
		print('VALUE ADDED TO VIEW COUNT: ', plus)
		
		
		count = result['view_count']
		print('before: ', count) 
		questionTable.update_one({'pid':pid}, { "$set": {'view_count': count + plus}} )
		print('after: ', count) 

		username =  result['username']
		title =  result['title']
		#media = result['media']
		body = result['body']
		timestamp =  result['time']
		tags = result['tags']
		view_count = result['view_count']
		userID = userTable.find_one({'username': username})['_id']
		userID = str(userID) 
		pid = str(pid)
		data = 	{
					'status': 'OK',	
					'question' :{
									'id': pid,
									'title':title,
									'body': body,
									'tags': tags,
									'answer_count': 0,
									'media': None,
									'accepted_answer_id': None,
									'user':	{	
												'username': username,
												'reputation': 0
											},
									'timestamp': timestamp,
									'score': 0,
									"view_count": count + plus
								}

				}
		return responseOK(data)

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
		



def responseOK(stat):
	data = stat
	jsonData = json.dumps(data)
	respond = Response(jsonData,status=200, mimetype='application/json')
	return respond
