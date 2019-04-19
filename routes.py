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
			answerReturn['answers'].append(str(result['_id']))
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


