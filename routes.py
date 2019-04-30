from flask import Blueprint, render_template, abort, Flask, request, url_for, json, redirect, Response, session, g,make_response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import  datetime
from flask_mail import Mail
from flask_mail import Message
import pymongo 
from pymongo import MongoClient
import time, random, string
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from bson.objectid import ObjectId
app = Flask(__name__)
client = MongoClient('130.245.170.76', 27017)

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
questionTable = db['question']
ipTable = db['ip']
upvoteTable = db['upvote']



from cassandra.cluster import Cluster
cluster = Cluster(['130.245.170.76'])
cassSession = cluster.connect(keyspace='hw5')
@bp.route('/', methods=['GET'])
@bp.route('/search', methods=['GET'])
def index():
	return redirect(url_for('question.searchOK'))



@bp.route('/questions/add', methods=["POST", "GET"])
def addQuestion():
	if request.method == "GET":
		return render_template('addQuestion.html')
	if(request.method == 'POST'):
		name = request.cookies.get('username')
		password = request.cookies.get('password')
		if is_login(name, password) == False:
			print('Add Question Wrong SESSION', (name, password))		
			return responseNO({'status': 'error', 'error': 'Wrong user session'})

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
						if name != request.cookies.get('username'):
							return responseOK({ 'status': 'error', 'error':"media does not belong to poster"}) 

		if ('title' in d) and ('body' in d) and ('tags' in d) :
			title = request.json['title'].encode("utf-8")
			body = request.json['body'].encode("utf-8")
			tags = request.json['tags']
		else:
			return responseOK({'status': 'error', 'error': 'Json key doesnt exist'})
				
		username = request.cookies.get('username')
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

@bp.route('/adduser', methods=["POST", "GET"])
def adduser():	
	if request.method == "GET":
		print("GET");
		return render_template('adduser.html')
	elif request.method == "POST":
		jss = request.json
		name = jss['username']
		email = jss['email']
		user_exist = userTable.find_one({'username': name})
		if user_exist != None :
			return responseNO({'status':'error', 'error': 'Duplicate user'})
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

		msg = MIMEText('validation key:<' + key +'>')
		msg["From"] = "ktube37@gmail.com"
		msg["To"] = email
		msg["Subject"] = "Hello"
		p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
		p.communicate(msg.as_string())
		return responseOK({'status':'OK'})



@bp.route('/verify', methods=["POST", "GET"])
def verify():
	if request.method == 'GET':
		return render_template('verify.html')
	elif request.method == 'POST':
		jss =request.json
		emailFilter = userTable.find_one({"email": jss['email']})
		if emailFilter == None:
			return responseNO({'status': 'error', 'error': 'Invalid email'})

		if(jss['key'] == 'abracadabra' or jss['key'] == 'keykey1212'):
			query = {'email' : jss['email']}
			newVal = {"$set": {"verified": "yes" }}  
			userTable.update_one(query, newVal)
		else:
			return responseNO({'status': 'error', 'error': 'Wrong key-email verification'})
		return responseOK({'status': 'OK'})

@bp.route('/login', methods=["POST", "GET"])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		print('==========*********************LOGIN')
		jss =request.json
		print(jss)
		name = str(jss['username'])
		get_user = userTable.find_one( { 'username': name } )
		if( get_user == None):
			return responseNO({'status': 'error', 'error':"Login user does not exist"})
			
		if get_user['password'] == jss['password'] and get_user['verified'] == 'yes':
			headers = {'Content-Type': 'application/json'}
			response = make_response(jsonify({"status": "OK"}), 200, headers)
			response.set_cookie('username', name)
			response.set_cookie('password', jss['password'])
			return response
		else:
			return responseNO({'status': 'error', 'error':"Wrong key-email pair"})


# @bp.route('/logout', methods=["POST", "GET"])
# def logout():
# 	if request.method =="POST":
# 		try:
# 			headers = {'Content-Type': 'application/json'}
# 			response = make_response(jsonify({"status": "OK"}), 200, headers)
# 			response.set_cookie('username', '', expires = 0)
# 			response.set_cookie('password', '', expires = 0)
# 			return response
# 		except Exception as e:
# 			return responseNO({'status': 'error'})


@bp.route('/user/<getName>', methods=["GET"])
def getUser(getName):
	if request.method == 'GET':
		username = str(getName)
		result = userTable.find_one({'username':username})
		if result == None:
			return responseNO({'status': 'error', 'error': 'User does not exist'})
		user ={	
					'email': result['email'],
					'reputation': result['reputation']
				}
		return responseOK({ 'status': 'OK', 'user': user}) 


@bp.route('/user/<getName>/questions', methods=["GET"])
def getUserQuestions(getName):
	if request.method == 'GET':
		username = str(getName)
		print(username)
		result = userTable.find_one({'username':username})
		if result == None:
			return responseNO({'status': 'error', 'error': 'USER DOESNT EXIST'})
		allQuestions = questionTable.find({ 'username': username } )
		questionReturn = {'status':'OK', 'questions': [] }

		for result in allQuestions:
			questionReturn['questions'].append(str(result['_id']))
		
		return responseOK(questionReturn)

@bp.route('/user/<getName>/answers', methods=["GET"])
def getUserAnnswer(getName):
	if request.method == 'GET':
		username = str(getName)
		print(username)
		result = userTable.find_one({'username':username})
		if result == None:
			print("/user/<getName>/answers : USER DOESNT EXIST")
			return responseOK({'status': 'error'})
		allAnswers = answerTable.find({ 'username': username } )
		answerReturn = {'status':'OK', 'answers': [] }

		for result in allAnswers:
			answerReturn['answers'].append(str(result['_id']))
		return responseOK(answerReturn)

@app.template_filter('ctime')
def timectime(s):
	return str(time.ctime(s))[3:19] # datetime.datetime.fromtimestamp(s)



@bp.route('/addmedia', methods=["POST"])
def addMedia():
	name = request.cookies.get('username')
	password = request.cookies.get('password')
	print('Add Media', (name, password))	
	if is_login(name, password) == False:
		print('Add Media User not logged in', (name, password))	
		return responseNO({'status': 'error', 'error': 'Please login to add media'})
	
	fileID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
	file = request.files.get('content')
	filetype = file.content_type

	b = bytearray(file.read())
	cqlinsert = "INSERT INTO imgs(fileID, content, filetype, username) VALUES (%s, %s, %s, %s);"
	cassSession.execute(cqlinsert, (fileID, b, filetype, name))
	return responseOK({'status': 'OK', 'id': fileID})

@bp.route('/media/<mediaID>', methods=["GET"])
def getMedia(mediaID):
	if request.method == 'GET':
		print("GET MEDIA ", mediaID)
		fileID = str(mediaID)
		query = "SELECT count(*) FROM imgs WHERE fileID = '" + fileID + "';"
		row = cassSession.execute(query)[0].count
		if row == 0:
			return responseNO({'status':'error', 'error': 'Media Id does not exist'})

		query = "SELECT * FROM imgs WHERE fileID = '" + fileID + "';"
		row = cassSession.execute(query)[0]
		file = row[1]
		filetype = row[2]
		response = make_response(file)
		response.headers.set('Content-Type', filetype)
		return response


@bp.route('/ginger', methods=["GET"])
def clean():
	import clean
	clean.clearMe()

	query = "SELECT count(*) FROM imgs;"
	cc = cassSession.execute(query)[0]
	print(cc)
	cqlinsert = "TRUNCATE imgs;"
	cassSession.execute(cqlinsert)
	return 'cleaned ' + str(cc)


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


def is_login(username, password):
	user = userTable.find_one({'username': username, 'password': password})
	if user == None:
		return False
	return True