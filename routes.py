from flask import Blueprint, render_template, abort
from flask import Flask, request, url_for, json, redirect, Response
from werkzeug.security import check_password_hash, generate_password_hash
import tictac, datetime
from flask_cors import CORS


bp = Blueprint('routes', __name__, template_folder='templates')
CORS(bp)
start = [0]

@bp.route('/', methods=['GET','POST'])
def index():
	return redirect(url_for('routes.adduser'))


@bp.route('/adduser', methods=["POST", "GET"])
#@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def adduser():	
	if request.method == "GET":
		print("GET");
		return render_template('adduser.html')
	elif request.method == "POST":
		print("Request Json =========================POST==========================")
		jsonObj = request.json
		username = jsonObj['username']
		email = jsonObj['email']
		password = jsonObj['password']
		
	data = {
			'status': 'OK'
	}
	jsonData = json.dumps(data)
	respond = Response(jsonData, status=200, mimetype='application/json')
	return respond




@bp.route('/verify/', methods=["POST", "GET"])
def verify():
	print("Verifyy Args==============================================================")
        jss =request.get_json()
        print(jss)
	
	#print(request.form.get('username') )
        #print(request.form.get('password') )
        #print(request.form.get('email') )

	data = {
                'status': 'OK'
        }
	jsonData = json.dumps(data)
        respond = Response(jsonData, status=200, mimetype='application/json')
        return respond

@bp.route('/login/', methods=["POST", "GET"])
def login():
	pass

@bp.route('/logout/', methods=["POST", "GET"])
def logout():
	pass

@bp.route('/listgames/', methods=["POST", "GET"])
def listgames():
	pass

@bp.route('/getgame/', methods=["POST", "GET"])
def getgame():
	pass

@bp.route('/getscore/', methods=["POST", "GET"])
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