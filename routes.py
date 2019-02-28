from flask import Blueprint, render_template, abort
from flask import Flask, request, url_for, json, redirect, Response
from werkzeug.security import check_password_hash, generate_password_hash
import tictac, datetime
from flask_cors import CORS
from flask_mail import Mail
from flask_mail import Message
import pymongo 
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client.wp2 
userTable = db['user']

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
start = [0]

tempEmail = None


@bp.route('/', methods=['GET','POST'])
def index():
	return redirect(url_for('routes.adduser'))


@bp.route('/adduser', methods=["POST", "GET"])
def adduser():	
	if request.method == "GET":
		print("GET");
		return render_template('adduser.html')
	elif request.method == "POST":
		print("Request Json =========================POST==========================")
		jsonObj = request.json
		print(jsonObj)
		userTable.insert( jsonObj)
		tempEmail = jsonObj['email']
	data = {
			'status': 'OK'
	}
	jsonData = json.dumps(data)
	respond = Response(jsonData, status=200, mimetype='application/json')
	return respond



@bp.route('/verify', methods=["POST", "GET"])
def verify():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		print("=========================VERIFY POST===============================")
		jss =request.json
		print("POST VERIFY JSON" , jss)

		query = {'email' : str(tempEmail)}
		newVal = {"$set": {"key": str(jss['key']) }}  
		msg = Message("Hello",sender="ktube110329@gmail.com", recipients=[jss['email']])
		msg.body = jss['key']
		mail.send(msg)
		if(jss['key'] != 'abracadabra'):
			return responseOK("ERROR")


		print("MESSAGE SENT*****************************************")
	
	return responseOK('OK')

@bp.route('/login', methods=["POST", "GET"])
def login():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		print("=========================LOGIN POST===============================")
		jss =request.json
		print("POST LOGIN JSON" , jss)
	

	return responseOK('OK')

@bp.route('/logout', methods=["POST", "GET"])
def logout():
	pass

@bp.route('/listgames', methods=["POST", "GET"])
def listgames():
	pass

@bp.route('/getgame', methods=["POST", "GET"])
def getgame():
	pass

@bp.route('/getscore', methods=["POST", "GET"])
def getscore():
	pass




@bp.route('/ttt/', methods=['GET','POST'])
def ttt():
	if request.method == 'POST':
		print("post")
		name = request.form['name']
		date =  datetime.date.today()
		return render_template('tic.html', name=name, date=date)
	
	return render_template('index.html')



@bp.route('/ttt/play', methods=['GET', 'POST'])
def play():
	jsonReceived = request.json
	print("updated ", jsonReceived)
	board = jsonReceived['grid'] # Array view of the board
	start[0]+=1


	if(tictac.findWinner(board)[0] ==  True ):
		return winningResponse(board, tictac.findWinner(board)[1] )#if human wins

	if(tictac.findWinner(board)[0] ==  False ):
		answer = tictac.getNextMove(board, start[0])
		
		if(answer[1]== 'O' ):
			return winningResponse(board, 'O') #if computer wins
		
		data = {
			'grid' : board,
			'winner' : ' '
		}
		jsonData = json.dumps(data)
		respond = Response(jsonData, status=200, mimetype='application/json')
		return respond






def winningResponse(board, winner):
	data = {
		'grid' : board,
		'winner' : winner
	}
	jsonData = json.dumps(data)
	respond = Response(jsonData, status=200, mimetype='application/json')
	return respond
def responseOK(stat):
	data = {'status': stat}
	jsonData = json.dumps(data)
	respond = Response(jsonData,status=200, mimetype='application/json')
	return respond